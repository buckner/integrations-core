# (C) Datadog, Inc. 2021-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

# This file is autogenerated.
# To change this file you should edit assets/configuration/spec.yaml and then run the following commands:
#     ddev -x validate config -s <INTEGRATION_NAME>
#     ddev -x validate models -s <INTEGRATION_NAME>


def instance_activity_metrics_excluded_aggregations():
    return []


def instance_application_name():
    return 'datadog-agent'


def instance_collect_activity_metrics():
    return False


def instance_collect_bloat_metrics():
    return False


def instance_collect_count_metrics():
    return True


def instance_collect_database_size_metrics():
    return True


def instance_collect_default_database():
    return True


def instance_collect_function_metrics():
    return False


def instance_collect_wal_metrics():
    return False


def instance_data_directory():
    return '/usr/local/pgsql/data'


def instance_database_instance_collection_interval():
    return False


def instance_dbm():
    return False


def instance_dbname():
    return 'postgres'


def instance_dbstrict():
    return False


def instance_disable_generic_tags():
    return False


def instance_empty_default_hostname():
    return False


def instance_idle_connection_timeout():
    return 60000


def instance_ignore_databases():
    return ['template%', 'rdsadmin', 'azure_maintenance']


def instance_log_unobfuscated_plans():
    return False


def instance_log_unobfuscated_queries():
    return False


def instance_max_connections():
    return 30


def instance_max_relations():
    return 300


def instance_min_collection_interval():
    return 15


def instance_pg_stat_statements_view():
    return 'show_pg_stat_statements()'


def instance_port():
    return 5432


def instance_query_timeout():
    return 5000


def instance_ssl():
    return 'disable'


def instance_table_count_limit():
    return 200


def instance_tag_replication_role():
    return False
