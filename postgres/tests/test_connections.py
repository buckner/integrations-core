# (C) Datadog, Inc. 2023-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import datetime
import pprint
import threading
import time
import uuid

import psycopg
import pytest
from psycopg.rows import dict_row

from datadog_checks.postgres import PostgreSql
from datadog_checks.postgres.connections import ConnectionPoolFullError, MultiDatabaseConnectionPool

from .common import HOST, PASSWORD_ADMIN, USER_ADMIN
from .utils import WaitGroup


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_conn_pool(pg_instance):
    """
    Test simple case of creating a connection pool, pruning a stale connection,
    and closing all connections.
    """
    check = PostgreSql('postgres', {}, [pg_instance])

    pool = MultiDatabaseConnectionPool(check, check._new_connection)
    with pool.get_connection('postgres', 1):
        assert pool._stats.connection_opened == 1
    time.sleep(0.001)

    # exiting the context block should set the connection to inactive
    # and it should be pruned
    pool.prune_connections()
    assert len(pool._conns) == 0
    assert pool._stats.connection_closed == 1
    assert pool._stats.connection_pruned == 1
    assert pool._stats.connection_closed_failed == 0

    db = pool._get_connection_raw('postgres', 999 * 1000)
    # run a simple query, and return conn object to the pool
    with db.cursor(row_factory=dict_row) as cursor:
        cursor.execute("select 1")
        rows = cursor.fetchall()
        assert len(rows) == 1 and list(rows[0].values())[0]
    assert len(pool._conns) == 1
    assert pool._stats.connection_opened == 2
    success = pool.close_all_connections()
    assert success
    assert len(pool._conns) == 0
    assert pool._stats.connection_closed == 2
    assert pool._stats.connection_closed_failed == 0
    assert pool._stats.connection_pruned == 1


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_conn_pool_no_leaks_on_close(pg_instance):
    """
    Test a simple case of opening and closing many connections. There should be no leaked connections on the server.
    """
    unique_id = str(uuid.uuid4())  # Used to isolate this test from others on the DB

    check = PostgreSql('postgres', {}, [pg_instance])
    check._config.application_name = unique_id

    # Used to make verification queries
    pool2 = MultiDatabaseConnectionPool(check, lambda dbname: local_db(dbname))

    # Iterate in the test many times to detect flakiness
    for _ in range(20):

        def exec_connection(pool, wg, dbname):
            with pool.get_connection(dbname, 10 * 1000) as conn:
                with conn.cursor(row_factory=dict_row) as cursor:
                    cursor.execute("select current_database()")
                    rows = cursor.fetchall()
                    assert len(rows) == 1
                    assert list(rows[0].values())[0] == dbname
                    wg.done()

        conn_count = 100
        threadpool = []
        pool = MultiDatabaseConnectionPool(check, check._new_connection)
        wg = WaitGroup()
        for i in range(conn_count):
            thread = threading.Thread(target=exec_connection, args=(pool, wg, 'dogs_{}'.format(i)))
            threadpool.append(thread)
            wg.add(1)
            thread.start()
        # wait for all connections to be opened
        wg.wait(timeout=5)
        assert pool._stats.connection_opened == conn_count
        assert len(get_activity(pool2, unique_id)) == conn_count

        pool.close_all_connections()
        assert pool._stats.connection_closed == conn_count
        assert pool._stats.connection_closed_failed == 0

        # Ensure all the connections have been terminated on the server
        attempts = 5
        while True:
            attempts -= 1

            rows = get_activity(pool2, unique_id)
            if len(rows) == 0:
                break

            assert attempts >= 0, "Connections leaked! Leaked rows found:\n{}".format(pprint.pformat(rows))
            time.sleep(1)


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_conn_pool_no_leaks_on_prune(pg_instance):
    """
    Test a scenario where many connections are created. These connections should be open on the database
    then should properly close on the pooler side and database when pruned and/or closed.
    """
    unique_id = str(uuid.uuid4())  # Used to isolate this test from others on the DB

    check = PostgreSql('postgres', {}, [pg_instance])
    check._config.application_name = unique_id

    pool = MultiDatabaseConnectionPool(check, check._new_connection)
    # Used to make verification queries
    pool2 = MultiDatabaseConnectionPool(check, lambda dbname: local_db(dbname))
    ttl_long = 90 * 1000
    ttl_short = 1

    def get_many_connections(count, ttl):
        """
        Retrieves the number of connections from the pool with the specified TTL
        """
        conn_pids = []
        for i in range(0, count):
            dbname = 'dogs_{}'.format(i)
            with pool.get_connection(dbname, ttl) as conn:
                with conn.cursor(row_factory=dict_row) as cursor:
                    cursor.execute("select current_database()")
                    rows = cursor.fetchall()
                    assert len(rows) == 1
                    assert list(rows[0].values())[0] == dbname
                    conn_pids.append(conn.info.backend_pid)
        return set(conn_pids)

    pool.close_all_connections()

    pool._stats.reset()

    # Create many connections with long-lived TTLs
    get_many_connections(50, ttl_long)
    assert len(pool._conns) == 50
    assert pool._stats.connection_opened == 50
    # Ensure those connections have the correct deadline and connection status
    for i in range(0, 50):
        dbname = 'dogs_{}'.format(i)
        conn_info = pool._conns[dbname]
        db = conn_info.connection
        deadline = conn_info.deadline
        approximate_deadline = datetime.datetime.now() + datetime.timedelta(milliseconds=ttl_long)
        assert (
            approximate_deadline - datetime.timedelta(seconds=1)
            < deadline
            < approximate_deadline + datetime.timedelta(seconds=1)
        )
        assert not db.closed
    # Check that those pooled connections do exist on the database
    rows = get_activity(pool2, unique_id)
    assert len(rows) == 50
    assert len({row['datname'] for row in rows}) == 50
    assert all(row['state'] == 'idle' for row in rows)
    pool._stats.reset()

    # Repeat this process many times and expect that only one connection is created per database
    for _ in range(100):
        conn_pids = get_many_connections(51, ttl_long)
        assert pool._stats.connection_opened == 1

        attempts_to_verify = 10
        # Loop here to prevent flakiness. Sometimes postgres doesn't immediately terminate backends.
        # The test can be considered successful as long as the backend is eventually terminated.
        for attempt in range(attempts_to_verify):
            rows = get_activity(pool2, unique_id)
            server_pids = {row['pid'] for row in rows}
            leaked_rows = [row for row in rows if row['pid'] in server_pids - conn_pids]
            if not leaked_rows:
                break
            if attempt < attempts_to_verify - 1:
                time.sleep(1)
                continue
            assert len(leaked_rows) == 0, 'Found leaked rows on the server not in the connection pool'

        assert len({row['datname'] for row in rows}) == 51
        assert len(rows) == 51, 'Possible leaked connections'
        assert all(row['state'] == 'idle' for row in rows)
    assert pool._stats.connection_opened == 1
    assert pool._stats.connection_closed == 0

    pool._stats.reset()

    # Now update db connections with short-lived TTLs and expect them to self-prune
    get_many_connections(55, ttl_short)
    time.sleep(0.001)
    pool.prune_connections()

    assert pool._stats.connection_opened == 55 - 51
    assert pool._stats.connection_closed == 55
    assert pool._stats.connection_pruned == 55
    assert pool._stats.connection_closed_failed == 0
    attempts_to_verify = 10
    for attempt in range(attempts_to_verify):
        leaked_rows = get_activity(pool2, unique_id)
        if attempt < attempts_to_verify - 1:
            time.sleep(1)
            continue
        assert len(leaked_rows) == 0, 'Found leaked rows remaining after TTL was updated to short TTL'

    # Final check that the server contains no leaked connections still open
    rows = get_activity(pool2, unique_id)
    assert len(rows) == 0


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_conn_pool_single_connection(pg_instance):
    """
    Test creating a single connection.
    """
    unique_id = str(uuid.uuid4())  # Used to isolate this test from others on the DB

    check = PostgreSql('postgres', {}, [pg_instance])
    check._config.application_name = unique_id

    # Used to make verification queries
    pool2 = MultiDatabaseConnectionPool(check, lambda dbname: local_db(dbname))

    pool = MultiDatabaseConnectionPool(check, check._new_connection)
    with pool.get_connection("dogs_0", 1000):
        pass

    assert pool._stats.connection_opened == 1
    assert len(get_activity(pool2, unique_id)) == 1

    expected_evicted = "dogs_0"
    evicted = pool.evict_lru()
    assert evicted == expected_evicted
    assert pool._stats.connection_closed == 1

    # ask for another connection again, error not raised
    with pool.get_connection("dogs_1", 1000):
        pass


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_conn_pool_manages_connections(pg_instance):
    """
    Test context manager API for connection grabbing.
    """

    def pretend_to_run_query(pool, dbname):
        with pool.get_connection(dbname, 10000):
            # release wait group & do some "work"
            # before exiting and setting the connection to inactive
            wg.done()
            time.sleep(5)

    limit = 30
    check = PostgreSql('postgres', {}, [pg_instance])

    pool = MultiDatabaseConnectionPool(check, check._new_connection, limit)
    threadpool = []
    wg = WaitGroup()
    for i in range(limit):
        thread = threading.Thread(target=pretend_to_run_query, args=(pool, 'dogs_{}'.format(i)))
        threadpool.append(thread)
        wg.add(1)
        thread.start()

    # wait until all connections are opened and active
    wg.wait(timeout=5)
    assert pool._stats.connection_opened == limit

    # ask for one more connection
    with pytest.raises(ConnectionPoolFullError):
        with pool.get_connection(dbname='dogs_{}'.format(limit + 1), ttl_ms=1, timeout=1):
            pass

    # join threads
    for thread in threadpool:
        thread.join()

    # now can add a new connection, one will get kicked out of pool
    with pool.get_connection('dogs_{}'.format(limit + 1), 60000):
        pass

    assert pool._stats.connection_closed == 1

    # close the rest
    pool.close_all_connections()
    assert pool._stats.connection_closed == limit + 1


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_conn_attempt_to_connect(pg_instance):
    """
    We attempt to connect to the database and check that the connection is successful.
    This test is meant to be run against a database that is not running.
    """
    # Change the password to something that is not the correct password
    pg_instance['password'] = 1234
    check = PostgreSql('postgres', {}, [pg_instance])
    with pytest.raises(psycopg.OperationalError):
        check._attempt_to_connect()


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_conn_kill_unexpectedly(pg_instance):
    """
    When a connection is killed by postgres server, db.closed will not be set.
    But the pool should not return this BAD connection.
    Instead, it should create a new connection.
    """
    check = PostgreSql('postgres', {}, [pg_instance])
    pool = MultiDatabaseConnectionPool(check, check._new_connection)
    pool2 = MultiDatabaseConnectionPool(check, lambda dbname: local_db(dbname))
    with pool._get_connection_raw(check._config.dbname, 10000):
        pass
    kill_postgres_connection(pool2, check._config.dbname)
    with pool.get_connection(check._config.dbname, 1) as conn:
        assert not conn.closed


def local_db(dbname):
    args = {
        'host': HOST,
        'user': USER_ADMIN,
        'password': PASSWORD_ADMIN,
        'dbname': dbname,
    }
    return psycopg.connect(**args)


def get_activity(db_pool, unique_id):
    """
    Fetches all pg_stat_activity rows generated by this test and connection to a "dogs%" database
    """
    with db_pool.get_connection('postgres', 1) as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                "SELECT pid, datname, usename, state, query_start, state_change, application_name"
                " FROM pg_stat_activity"
                " WHERE datname LIKE 'dogs%%' AND application_name = %s",
                (unique_id,),
            )
            return cursor.fetchall()


def kill_postgres_connection(db_pool, dbname):
    """
    Kills all connections to a database except the current connection
    """
    with db_pool.get_connection('postgres', 1) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT pg_terminate_backend(pid)"
                " FROM pg_stat_activity"
                " WHERE datname = %s AND pid <> pg_backend_pid()",
                (dbname,),
            )
