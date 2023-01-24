# (C) Datadog, Inc. 2018-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import os

from datadog_checks.base.utils.common import get_docker_hostname

HERE = os.path.dirname(os.path.abspath(__file__))

# Networking
HOST = get_docker_hostname()
PORT = '8091'
QUERY_PORT = '8093'
SG_PORT = '4985'
INDEX_STATS_PORT = '9102'

# Tags and common bucket name
CUSTOM_TAGS = ['optional:tag1']
CHECK_TAGS = CUSTOM_TAGS + ['instance:http://{}:{}'.format(HOST, PORT)]
BUCKET_NAME = 'cb_bucket'
INDEX_STATS_TAGS = CHECK_TAGS + [
    'bucket:cb_bucket',
    'collection:default',
    'index_name:gamesim_primary',
    'scope:default',
]

URL = 'http://{}:{}'.format(HOST, PORT)
QUERY_URL = 'http://{}:{}'.format(HOST, QUERY_PORT)
SG_URL = 'http://{}:{}'.format(HOST, SG_PORT)
INDEX_STATS_URL = 'http://{}:{}'.format(HOST, INDEX_STATS_PORT)
CB_CONTAINER_NAME = 'couchbase-standalone'
USER = 'Administrator'
PASSWORD = 'password'

COUCHBASE_MAJOR_VERSION = int(os.getenv('COUCHBASE_VERSION').split(".")[0])

DEFAULT_INSTANCE = {'server': URL, 'user': USER, 'password': PASSWORD, 'timeout': 1, 'tags': CUSTOM_TAGS}

SYNC_GATEWAY_METRICS = [
    "couchbase.sync_gateway.admin_net_bytes_recv",
    "couchbase.sync_gateway.admin_net_bytes_sent",
    "couchbase.sync_gateway.cache.abandoned_seqs",
    "couchbase.sync_gateway.cache.chan_cache_active_revs",
    "couchbase.sync_gateway.cache.chan_cache_bypass_count",
    "couchbase.sync_gateway.cache.chan_cache_channels_added",
    "couchbase.sync_gateway.cache.chan_cache_channels_evicted_inactive",
    "couchbase.sync_gateway.cache.chan_cache_channels_evicted_nru",
    "couchbase.sync_gateway.cache.chan_cache_compact_count",
    "couchbase.sync_gateway.cache.chan_cache_compact_time",
    "couchbase.sync_gateway.cache.chan_cache_hits",
    "couchbase.sync_gateway.cache.chan_cache_max_entries",
    "couchbase.sync_gateway.cache.chan_cache_misses",
    "couchbase.sync_gateway.cache.chan_cache_num_channels",
    "couchbase.sync_gateway.cache.chan_cache_pending_queries",
    "couchbase.sync_gateway.cache.chan_cache_removal_revs",
    "couchbase.sync_gateway.cache.chan_cache_tombstone_revs",
    "couchbase.sync_gateway.cache.high_seq_cached",
    "couchbase.sync_gateway.cache.high_seq_stable",
    "couchbase.sync_gateway.cache.num_active_channels",
    "couchbase.sync_gateway.cache.num_skipped_seqs",
    "couchbase.sync_gateway.cache.pending_seq_len",
    "couchbase.sync_gateway.cache.rev_cache_bypass",
    "couchbase.sync_gateway.cache.rev_cache_hits",
    "couchbase.sync_gateway.cache.rev_cache_misses",
    "couchbase.sync_gateway.cache.skipped_seq_len",
    "couchbase.sync_gateway.cbl_replication_pull.attachment_pull_bytes",
    "couchbase.sync_gateway.cbl_replication_pull.attachment_pull_count",
    "couchbase.sync_gateway.cbl_replication_pull.max_pending",
    "couchbase.sync_gateway.cbl_replication_pull.num_pull_repl_active_continuous",
    "couchbase.sync_gateway.cbl_replication_pull.num_pull_repl_active_one_shot",
    "couchbase.sync_gateway.cbl_replication_pull.num_pull_repl_caught_up",
    "couchbase.sync_gateway.cbl_replication_pull.num_pull_repl_since_zero",
    "couchbase.sync_gateway.cbl_replication_pull.num_pull_repl_total_continuous",
    "couchbase.sync_gateway.cbl_replication_pull.num_pull_repl_total_one_shot",
    "couchbase.sync_gateway.cbl_replication_pull.num_replications_active",
    "couchbase.sync_gateway.cbl_replication_pull.request_changes_count",
    "couchbase.sync_gateway.cbl_replication_pull.request_changes_time",
    "couchbase.sync_gateway.cbl_replication_pull.rev_processing_time",
    "couchbase.sync_gateway.cbl_replication_pull.rev_send_count",
    "couchbase.sync_gateway.cbl_replication_pull.rev_send_latency",
    "couchbase.sync_gateway.cbl_replication_push.attachment_push_bytes",
    "couchbase.sync_gateway.cbl_replication_push.attachment_push_count",
    "couchbase.sync_gateway.cbl_replication_push.doc_push_count",
    "couchbase.sync_gateway.cbl_replication_push.propose_change_count",
    "couchbase.sync_gateway.cbl_replication_push.propose_change_time",
    "couchbase.sync_gateway.cbl_replication_push.sync_function_count",
    "couchbase.sync_gateway.cbl_replication_push.sync_function_time",
    "couchbase.sync_gateway.cbl_replication_push.write_processing_time",
    "couchbase.sync_gateway.database.abandoned_seqs",
    "couchbase.sync_gateway.database.conflict_write_count",
    "couchbase.sync_gateway.database.crc32c_match_count",
    "couchbase.sync_gateway.database.dcp_caching_count",
    "couchbase.sync_gateway.database.dcp_caching_time",
    "couchbase.sync_gateway.database.dcp_received_count",
    "couchbase.sync_gateway.database.dcp_received_time",
    "couchbase.sync_gateway.database.doc_reads_bytes_blip",
    "couchbase.sync_gateway.database.doc_writes_bytes",
    "couchbase.sync_gateway.database.doc_writes_bytes_blip",
    "couchbase.sync_gateway.database.doc_writes_xattr_bytes",
    "couchbase.sync_gateway.database.high_seq_feed",
    "couchbase.sync_gateway.database.num_doc_reads_blip",
    "couchbase.sync_gateway.database.num_doc_reads_rest",
    "couchbase.sync_gateway.database.num_doc_writes",
    "couchbase.sync_gateway.database.num_replications_active",
    "couchbase.sync_gateway.database.num_replications_total",
    "couchbase.sync_gateway.database.num_tombstones_compacted",
    "couchbase.sync_gateway.database.sequence_assigned_count",
    "couchbase.sync_gateway.database.sequence_get_count",
    "couchbase.sync_gateway.database.sequence_incr_count",
    "couchbase.sync_gateway.database.sequence_released_count",
    "couchbase.sync_gateway.database.sequence_reserved_count",
    "couchbase.sync_gateway.database.warn_channels_per_doc_count",
    "couchbase.sync_gateway.database.warn_grants_per_doc_count",
    "couchbase.sync_gateway.database.warn_xattr_size_count",
    "couchbase.sync_gateway.error_count",
    "couchbase.sync_gateway.go_memstats_heapalloc",
    "couchbase.sync_gateway.go_memstats_heapidle",
    "couchbase.sync_gateway.go_memstats_heapinuse",
    "couchbase.sync_gateway.go_memstats_heapreleased",
    "couchbase.sync_gateway.go_memstats_pausetotalns",
    "couchbase.sync_gateway.go_memstats_stackinuse",
    "couchbase.sync_gateway.go_memstats_stacksys",
    "couchbase.sync_gateway.go_memstats_sys",
    "couchbase.sync_gateway.goroutines_high_watermark",
    "couchbase.sync_gateway.num_goroutines",
    "couchbase.sync_gateway.process_cpu_percent_utilization",
    "couchbase.sync_gateway.process_memory_resident",
    "couchbase.sync_gateway.pub_net_bytes_recv",
    "couchbase.sync_gateway.pub_net_bytes_sent",
    "couchbase.sync_gateway.security.auth_failed_count",
    "couchbase.sync_gateway.security.auth_success_count",
    "couchbase.sync_gateway.security.num_access_errors",
    "couchbase.sync_gateway.security.num_docs_rejected",
    "couchbase.sync_gateway.security.total_auth_time",
    "couchbase.sync_gateway.shared_bucket_import.import_cancel_cas",
    "couchbase.sync_gateway.shared_bucket_import.import_count",
    "couchbase.sync_gateway.shared_bucket_import.import_error_count",
    "couchbase.sync_gateway.shared_bucket_import.import_high_seq",
    "couchbase.sync_gateway.shared_bucket_import.import_partitions",
    "couchbase.sync_gateway.shared_bucket_import.import_processing_time",
    "couchbase.sync_gateway.system_memory_total",
    "couchbase.sync_gateway.warn_count",
]

INDEX_STATS_INDEXER_METRICS = [
    'couchbase.indexer.indexer_state',
    'couchbase.indexer.memory_quota',
    'couchbase.indexer.memory_total_storage',
    'couchbase.indexer.memory_used',
    'couchbase.indexer.total_indexer_gc_pause_ns',
]

INDEX_STATS_GAUGE_METRICS = [
    'couchbase.index.avg_drain_rate',
    'couchbase.index.avg_item_size',
    'couchbase.index.avg_scan_latency',
    'couchbase.index.cache_hit_percent',
    'couchbase.index.data_size',
    'couchbase.index.disk_size',
    'couchbase.index.frag_percent',
    'couchbase.index.initial_build_progress',
    'couchbase.index.last_known_scan_time',
    'couchbase.index.num_docs_pending',
    'couchbase.index.num_docs_queued',
    'couchbase.index.num_pending_requests',
    'couchbase.index.recs_in_mem',
    'couchbase.index.recs_on_disk',
    'couchbase.index.resident_percent',
    'couchbase.index.total_scan_duration',
]

INDEX_STATS_COUNT_METRICS = [
    'couchbase.index.cache_hits',
    'couchbase.index.cache_misses',
    'couchbase.index.items_count',
    'couchbase.index.num_docs_indexed',
    'couchbase.index.num_items_flushed',
    'couchbase.index.num_requests',
    'couchbase.index.num_rows_returned',
    'couchbase.index.num_scan_errors',
    'couchbase.index.num_scan_timeouts',
    'couchbase.index.scan_bytes_read',
]

QUERY_STATS_ALWAYS_PRESENT = {
    'cores',
    'cpu_sys_percent',
    'cpu_user_percent',
    'memory_total',
    'request_per_sec_15min',
    'request_per_sec_1min',
    'request_per_sec_5min',
    'request_prepared_percent',
}

BY_BUCKET_METRICS = [
    'couchbase.by_bucket.ep_overhead',
    'couchbase.by_bucket.ep_queue_size',
    'couchbase.by_bucket.ep_vb_total',
    'couchbase.by_bucket.mem_used',
    'couchbase.by_bucket.vb_active_itm_memory',
    'couchbase.by_bucket.vb_active_meta_data_memory',
    'couchbase.by_bucket.vb_active_num',
    'couchbase.by_bucket.vb_active_num_non_resident',
    'couchbase.by_bucket.vb_active_queue_age',
    'couchbase.by_bucket.vb_active_queue_size',
    'couchbase.by_bucket.vb_pending_curr_items',
    'couchbase.by_bucket.vb_pending_itm_memory',
    'couchbase.by_bucket.vb_pending_meta_data_memory',
    'couchbase.by_bucket.vb_pending_num',
    'couchbase.by_bucket.vb_pending_num_non_resident',
    'couchbase.by_bucket.vb_pending_queue_age',
    'couchbase.by_bucket.vb_pending_queue_size',
    'couchbase.by_bucket.vb_replica_curr_items',
    'couchbase.by_bucket.vb_replica_itm_memory',
    'couchbase.by_bucket.vb_replica_meta_data_memory',
    'couchbase.by_bucket.vb_replica_num',
    'couchbase.by_bucket.vb_replica_num_non_resident',
    'couchbase.by_bucket.vb_replica_queue_age',
    'couchbase.by_bucket.vb_replica_queue_size',
    'couchbase.by_bucket.vb_total_queue_age',
]

OPTIONAL_BY_BUCKET_METRICS = [
    'couchbase.by_bucket.avg_bg_wait_time',
    'couchbase.by_bucket.avg_disk_commit_time',
    'couchbase.by_bucket.avg_disk_update_time',
    'couchbase.by_bucket.bg_wait_total',
    'couchbase.by_bucket.bytes_read',
    'couchbase.by_bucket.bytes_written',
    'couchbase.by_bucket.cas_badval',
    'couchbase.by_bucket.cas_hits',
    'couchbase.by_bucket.cas_misses',
    'couchbase.by_bucket.cmd_get',
    'couchbase.by_bucket.cmd_set',
    'couchbase.by_bucket.couch_docs_actual_disk_size',
    'couchbase.by_bucket.couch_spatial_data_size',
    'couchbase.by_bucket.couch_spatial_disk_size',
    'couchbase.by_bucket.couch_spatial_ops',
    'couchbase.by_bucket.couch_total_disk_size',
    'couchbase.by_bucket.couch_views_data_size',
    'couchbase.by_bucket.couch_views_disk_size',
    'couchbase.by_bucket.couch_views_fragmentation',
    'couchbase.by_bucket.couch_views_ops',
    'couchbase.by_bucket.decr_hits',
    'couchbase.by_bucket.decr_misses',
    'couchbase.by_bucket.delete_hits',
    'couchbase.by_bucket.delete_misses',
    'couchbase.by_bucket.disk_commit_count',
    'couchbase.by_bucket.disk_update_count',
    'couchbase.by_bucket.ep_bg_fetched',
    'couchbase.by_bucket.ep_cache_miss_rate',
    'couchbase.by_bucket.ep_cache_miss_ratio',
    'couchbase.by_bucket.ep_dcp_2i_backoff',
    'couchbase.by_bucket.ep_dcp_2i_count',
    'couchbase.by_bucket.ep_dcp_2i_items_remaining',
    'couchbase.by_bucket.ep_dcp_2i_items_sent',
    'couchbase.by_bucket.ep_dcp_2i_producer_count',
    'couchbase.by_bucket.ep_dcp_2i_total_bytes',
    'couchbase.by_bucket.ep_dcp_fts_backoff',
    'couchbase.by_bucket.ep_dcp_fts_count',
    'couchbase.by_bucket.ep_dcp_fts_items_remaining',
    'couchbase.by_bucket.ep_dcp_fts_items_sent',
    'couchbase.by_bucket.ep_dcp_fts_producer_count',
    'couchbase.by_bucket.ep_dcp_fts_total_bytes',
    'couchbase.by_bucket.ep_dcp_other_backoff',
    'couchbase.by_bucket.ep_dcp_other_count',
    'couchbase.by_bucket.ep_dcp_other_items_remaining',
    'couchbase.by_bucket.ep_dcp_other_items_sent',
    'couchbase.by_bucket.ep_dcp_other_producer_count',
    'couchbase.by_bucket.ep_dcp_other_total_bytes',
    'couchbase.by_bucket.ep_dcp_replica_backoff',
    'couchbase.by_bucket.ep_dcp_replica_count',
    'couchbase.by_bucket.ep_dcp_replica_items_remaining',
    'couchbase.by_bucket.ep_dcp_replica_items_sent',
    'couchbase.by_bucket.ep_dcp_replica_producer_count',
    'couchbase.by_bucket.ep_dcp_replica_total_bytes',
    'couchbase.by_bucket.ep_dcp_views_backoff',
    'couchbase.by_bucket.ep_dcp_views_count',
    'couchbase.by_bucket.ep_dcp_views_items_remaining',
    'couchbase.by_bucket.ep_dcp_views_items_sent',
    'couchbase.by_bucket.ep_dcp_views_producer_count',
    'couchbase.by_bucket.ep_dcp_views_total_bytes',
    'couchbase.by_bucket.ep_dcp_xdcr_backoff',
    'couchbase.by_bucket.ep_dcp_xdcr_count',
    'couchbase.by_bucket.ep_dcp_xdcr_items_remaining',
    'couchbase.by_bucket.ep_dcp_xdcr_items_sent',
    'couchbase.by_bucket.ep_dcp_xdcr_producer_count',
    'couchbase.by_bucket.ep_dcp_xdcr_total_bytes',
    'couchbase.by_bucket.ep_diskqueue_drain',
    'couchbase.by_bucket.ep_diskqueue_fill',
    'couchbase.by_bucket.ep_max_size',
    'couchbase.by_bucket.ep_mem_high_wat',
    'couchbase.by_bucket.ep_oom_errors',
    'couchbase.by_bucket.ep_tap_replica_queue_drain',
    'couchbase.by_bucket.ep_tap_total_queue_drain',
    'couchbase.by_bucket.ep_tap_total_queue_fill',
    'couchbase.by_bucket.ep_tap_total_total_backlog_size',
    'couchbase.by_bucket.hit_ratio',
    'couchbase.by_bucket.page_faults',
    'couchbase.by_bucket.replication_docs_rep_queue',
    'couchbase.by_bucket.replication_meta_latency_aggr',
]

if COUCHBASE_MAJOR_VERSION == 5:
    BY_BUCKET_METRICS += [
        'couchbase.by_bucket.couch_docs_fragmentation',
        'couchbase.by_bucket.cpu_idle_ms',
        'couchbase.by_bucket.cpu_utilization_rate',
        'couchbase.by_bucket.ep_mem_low_wat',
        'couchbase.by_bucket.ep_meta_data_memory',
        'couchbase.by_bucket.ep_num_non_resident',
        'couchbase.by_bucket.ep_num_ops_del_meta',
        'couchbase.by_bucket.ep_num_ops_del_ret_meta',
        'couchbase.by_bucket.ep_num_ops_get_meta',
        'couchbase.by_bucket.ep_num_ops_set_meta',
        'couchbase.by_bucket.ep_num_ops_set_ret_meta',
        'couchbase.by_bucket.ep_num_value_ejects',
        'couchbase.by_bucket.ep_ops_create',
        'couchbase.by_bucket.ep_ops_update',
        'couchbase.by_bucket.ep_tmp_oom_errors',
        'couchbase.by_bucket.evictions',
        'couchbase.by_bucket.get_hits',
        'couchbase.by_bucket.get_misses',
        'couchbase.by_bucket.hibernated_requests',
        'couchbase.by_bucket.hibernated_waked',
        'couchbase.by_bucket.incr_hits',
        'couchbase.by_bucket.incr_misses',
        'couchbase.by_bucket.mem_actual_free',
        'couchbase.by_bucket.mem_actual_used',
        'couchbase.by_bucket.mem_free',
        'couchbase.by_bucket.mem_total',
        'couchbase.by_bucket.mem_used_sys',
        'couchbase.by_bucket.misses',
        'couchbase.by_bucket.ops',
        'couchbase.by_bucket.rest_requests',
        'couchbase.by_bucket.swap_total',
        'couchbase.by_bucket.swap_used',
        'couchbase.by_bucket.vb_active_eject',
        'couchbase.by_bucket.vb_active_ops_create',
        'couchbase.by_bucket.vb_active_ops_update',
        'couchbase.by_bucket.vb_active_queue_drain',
        'couchbase.by_bucket.vb_active_queue_fill',
        'couchbase.by_bucket.vb_pending_eject',
        'couchbase.by_bucket.vb_pending_ops_create',
        'couchbase.by_bucket.vb_pending_ops_update',
        'couchbase.by_bucket.vb_pending_queue_drain',
        'couchbase.by_bucket.vb_pending_queue_fill',
        'couchbase.by_bucket.vb_replica_eject',
        'couchbase.by_bucket.vb_replica_ops_create',
        'couchbase.by_bucket.vb_replica_ops_update',
        'couchbase.by_bucket.vb_replica_queue_drain',
        'couchbase.by_bucket.vb_replica_queue_fill',
        'couchbase.by_bucket.xdc_ops',
    ]
    OPTIONAL_BY_BUCKET_METRICS += [
        'couchbase.by_bucket.couch_docs_data_size',
        'couchbase.by_bucket.couch_docs_disk_size',
        'couchbase.by_bucket.curr_connections',
        'couchbase.by_bucket.curr_items',
        'couchbase.by_bucket.curr_items_tot',
        'couchbase.by_bucket.disk_write_queue',
        'couchbase.by_bucket.ep_diskqueue_items',
        'couchbase.by_bucket.ep_flusher_todo',
        'couchbase.by_bucket.ep_item_commit_failed',
        'couchbase.by_bucket.ep_kv_size',
        'couchbase.by_bucket.ep_resident_items_rate',
        'couchbase.by_bucket.vb_active_resident_items_ratio',
        'couchbase.by_bucket.vb_avg_active_queue_age',
        'couchbase.by_bucket.vb_avg_pending_queue_age',
        'couchbase.by_bucket.vb_avg_replica_queue_age',
        'couchbase.by_bucket.vb_avg_total_queue_age',
        'couchbase.by_bucket.vb_pending_resident_items_ratio',
        'couchbase.by_bucket.vb_replica_resident_items_ratio',
    ]
elif COUCHBASE_MAJOR_VERSION == 7:
    BY_BUCKET_METRICS += [
        'couchbase.by_bucket.couch_docs_data_size',
        'couchbase.by_bucket.couch_docs_disk_size',
        'couchbase.by_bucket.curr_connections',
        'couchbase.by_bucket.curr_items',
        'couchbase.by_bucket.curr_items_tot',
        'couchbase.by_bucket.disk_write_queue',
        'couchbase.by_bucket.ep_diskqueue_items',
        'couchbase.by_bucket.ep_flusher_todo',
        'couchbase.by_bucket.ep_item_commit_failed',
        'couchbase.by_bucket.ep_kv_size',
        'couchbase.by_bucket.ep_resident_items_rate',
        'couchbase.by_bucket.vb_active_resident_items_ratio',
        'couchbase.by_bucket.vb_avg_active_queue_age',
        'couchbase.by_bucket.vb_avg_pending_queue_age',
        'couchbase.by_bucket.vb_avg_replica_queue_age',
        'couchbase.by_bucket.vb_avg_total_queue_age',
        'couchbase.by_bucket.vb_pending_resident_items_ratio',
        'couchbase.by_bucket.vb_replica_resident_items_ratio',
    ]
    OPTIONAL_BY_BUCKET_METRICS += [
        'couchbase.by_bucket.couch_docs_fragmentation',
        'couchbase.by_bucket.cpu_idle_ms',
        'couchbase.by_bucket.cpu_utilization_rate',
        'couchbase.by_bucket.ep_mem_low_wat',
        'couchbase.by_bucket.ep_meta_data_memory',
        'couchbase.by_bucket.ep_num_non_resident',
        'couchbase.by_bucket.ep_num_ops_del_meta',
        'couchbase.by_bucket.ep_num_ops_del_ret_meta',
        'couchbase.by_bucket.ep_num_ops_get_meta',
        'couchbase.by_bucket.ep_num_ops_set_meta',
        'couchbase.by_bucket.ep_num_ops_set_ret_meta',
        'couchbase.by_bucket.ep_num_value_ejects',
        'couchbase.by_bucket.ep_ops_create',
        'couchbase.by_bucket.ep_ops_update',
        'couchbase.by_bucket.ep_tmp_oom_errors',
        'couchbase.by_bucket.evictions',
        'couchbase.by_bucket.get_hits',
        'couchbase.by_bucket.get_misses',
        'couchbase.by_bucket.hibernated_requests',
        'couchbase.by_bucket.hibernated_waked',
        'couchbase.by_bucket.incr_hits',
        'couchbase.by_bucket.incr_misses',
        'couchbase.by_bucket.mem_actual_free',
        'couchbase.by_bucket.mem_actual_used',
        'couchbase.by_bucket.mem_free',
        'couchbase.by_bucket.mem_total',
        'couchbase.by_bucket.mem_used_sys',
        'couchbase.by_bucket.misses',
        'couchbase.by_bucket.ops',
        'couchbase.by_bucket.rest_requests',
        'couchbase.by_bucket.swap_total',
        'couchbase.by_bucket.swap_used',
        'couchbase.by_bucket.vb_active_eject',
        'couchbase.by_bucket.vb_active_ops_create',
        'couchbase.by_bucket.vb_active_ops_update',
        'couchbase.by_bucket.vb_active_queue_drain',
        'couchbase.by_bucket.vb_active_queue_fill',
        'couchbase.by_bucket.vb_pending_eject',
        'couchbase.by_bucket.vb_pending_ops_create',
        'couchbase.by_bucket.vb_pending_ops_update',
        'couchbase.by_bucket.vb_pending_queue_drain',
        'couchbase.by_bucket.vb_pending_queue_fill',
        'couchbase.by_bucket.vb_replica_eject',
        'couchbase.by_bucket.vb_replica_ops_create',
        'couchbase.by_bucket.vb_replica_ops_update',
        'couchbase.by_bucket.vb_replica_queue_drain',
        'couchbase.by_bucket.vb_replica_queue_fill',
        'couchbase.by_bucket.xdc_ops',
    ]


NODE_STATS = [
    'cmd_get',
    'curr_items',
    'curr_items_tot',
    'couch_docs_data_size',
    'couch_docs_actual_disk_size',
    'couch_spatial_data_size',
    'couch_spatial_disk_size',
    'couch_views_data_size',
    'couch_views_actual_disk_size',
    'ep_bg_fetched',
    'get_hits',
    'mem_used',
    'ops',
    'vb_active_num_non_resident',
    'vb_replica_curr_items',
]

if COUCHBASE_MAJOR_VERSION == 7:
    NODE_STATS += ['index_data_size', 'index_disk_size']

TOTAL_STATS = [
    'hdd.free',
    'hdd.used',
    'hdd.total',
    'hdd.quota_total',
    'hdd.used_by_data',
    'ram.used',
    'ram.total',
    'ram.quota_total',
    'ram.quota_total_per_node',
    'ram.quota_used_per_node',
    'ram.quota_used',
    'ram.used_by_data',
]

BUCKET_TAGS = CHECK_TAGS + ['bucket:{}'.format(BUCKET_NAME)]


def _assert_bucket_metrics(aggregator, tags, device=None):
    for metric in BY_BUCKET_METRICS:
        aggregator.assert_metric(metric, tags=tags, device=device, count=1)

    for metric in OPTIONAL_BY_BUCKET_METRICS:
        aggregator.assert_metric(metric, tags=tags, device=device, at_least=0)


def _assert_stats(aggregator, node_tags, device=None):
    for mname in NODE_STATS:
        aggregator.assert_metric('couchbase.by_node.{}'.format(mname), tags=node_tags, count=1, device=device)
    # Assert 'couchbase.' metrics
    for mname in TOTAL_STATS:
        aggregator.assert_metric('couchbase.{}'.format(mname), tags=CHECK_TAGS, count=1)
