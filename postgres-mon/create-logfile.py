import os
import subprocess

zabbix_server='10.10.10.86'
password = '123456789'
host = '10.10.10.128'
ports = [5433]
hostname = '"jiratest"'

commands = ["\"select count(*) from pg_buffercache where not isdirty\"",
            "\"select count(*) from pg_buffercache where isdirty\"",
            "\"select count(*) from pg_buffercache where reldatabase is not null\"",
            "\"select count(*) from pg_buffercache\"",
            "\"select buffers_checkpoint from pg_stat_bgwriter\"",
            "\"select checkpoints_timed from pg_stat_bgwriter\"",
            "\"select coalesce(extract(epoch from max(age(now(), query_start))), 0) from pg_stat_activity where state='idle in transaction'\"",
            "\"select coalesce(extract(epoch from max(age(now(), query_start))), 0) from pg_stat_activity where state <> 'idle in transaction' and state <> 'idle'\"",
            "\"select coalesce(extract(epoch from max(age(now(), query_start))), 0) from pg_stat_activity WHERE backend_type = 'client backend' AND state != 'idle' AND wait_event IS NOT NULL\"",
            "\"select coalesce(extract(epoch from max(age(now(), prepared))), 0) from pg_prepared_xacts\"",
            "\"select count(*) from pg_stat_activity where state = 'active'\"",
            "\"select count(*) from pg_stat_activity where state = 'idle'\"",
            "\"select count(*) from pg_stat_activity where state = 'idle in transaction'\"",
            "\"select count(*) from pg_stat_activity\"",
            "\"select count(*)*100/(select current_setting('max_connections')::int) from pg_stat_activity\"",
            "\"select count(*) from pg_stat_activity WHERE backend_type = 'client backend' AND state != 'idle' AND wait_event IS NOT NULL;\"",
            "\"select count(*) from pg_prepared_xacts\"",
            "\"select checkpoints_timed from pg_stat_bgwriter\"",
            "\"select checkpoints_req from pg_stat_bgwriter\"",
            "\"select checkpoint_write_time from pg_stat_bgwriter\"",
            "\"select checkpoint_sync_time from pg_stat_bgwriter\"",
            "\"select buffers_checkpoint from pg_stat_bgwriter\"",
            "\"select buffers_clean from pg_stat_bgwriter\"",
            "\"select maxwritten_clean from pg_stat_bgwriter\"",
            "\"select buffers_backend from pg_stat_bgwriter\"",
            "\"select buffers_backend_fsync from pg_stat_bgwriter\"",
            "\"select buffers_alloc from pg_stat_bgwriter\"",
            "\"select sum(blks_hit) from pg_stat_database\"",
            "\"select sum(blks_read) from pg_stat_database\"",
            "\"select sum(xact_commit) from pg_stat_database\"",
            "\"select sum(conflicts) from pg_stat_database\"",
            "\"select sum(deadlocks) from pg_stat_database\"",
            "\"select sum(xact_rollback) from pg_stat_database\"",
            "\"select sum(temp_bytes) from pg_stat_database\"",
            "\"select sum(temp_files) from pg_stat_database\"",
            "\"select sum(tup_deleted) from pg_stat_database\"",
            "\"select sum(tup_fetched) from pg_stat_database\"",
            "\"select sum(tup_inserted) from pg_stat_database\"",
            "\"select sum(tup_returned) from pg_stat_database\"",
            "\"select sum(tup_updated) from pg_stat_database\""

            ]


for port in ports:
    f = open('postgres_log_port_%s.log'%port, 'w')
    f.flush()
    keys = ['postgres[%s,clear]' % port,
            'postgres[%s,dirty]' % port,
            'postgres[%s,used]' % port,
            'postgres[%s,total-buffers]' % port,
            'postgres[%s,buffer-write]' % port,
            'postgres[%s,checkpoints-timed]' % port,
            'postgres[%s,idle-transaction]' % port,
            'postgres[%s,active-transaction]' % port,
            'postgres[%s,waiting-transaction]' % port,
            'postgres[%s,prepared-transaction]' % port,
            'postgres[%s,active-connection]' % port,
            'postgres[%s,idle-connection]' % port,
            'postgres[%s,idle_in_transaction]' % port,
            'postgres[%s,total_connection]' % port,
            'postgres[%s,total_connection_pct]' % port,
            'postgres[%s,waiting_connection]' % port,
            'postgres[%s,prepared_connection]' % port,
            'postgres[%s,checkpoint_timeout]' % port,
            'postgres[%s,checkpoints_req]' % port,
            'postgres[%s,checkpoint_write_time]' % port,
            'postgres[%s,checkpoint_sync_time]' % port,
            'postgres[%s,buffers_checkpoint]' % port,
            'postgres[%s,buffers_clean]' % port,
            'postgres[%s,maxwritten_clean]' % port,
            'postgres[%s,buffers_backend]' % port,
            'postgres[%s,buffers_backend_fsync]' % port,
            'postgres[%s,buffers_alloc]' % port,
            'postgres[%s,sum_blks_hit]' % port,
            'postgres[%s,sum_blks_read]' % port,
            'postgres[%s,sum_xact_commit]' % port,
            'postgres[%s,sum_conflicts]' % port,
            'postgres[%s,sum_deadlocks]' % port,
            'postgres[%s,sum_xact_rollback]' % port,
            'postgres[%s,sum_temp_bytes]' % port,
            'postgres[%s,sum_temp_files]' % port,
            'postgres[%s,sum_tup_deleted]' % port,
            'postgres[%s,sum_tup_fetched]' % port,
            'postgres[%s,sum_tup_inserted]' % port,
            'postgres[%s,sum_tup_returned]' % port,
            'postgres[%s,sum_tup_updated]' % port

            ]
    for key, command in zip(keys, commands):
        value = subprocess.getoutput(
            "PGPASSWORD=%s psql -qAtX -h %s -p %s -U zabbix -c %s" % (password, host, port, command))
        print(hostname, key, value)
        # print(keys.index(key))
        f.write('%s %s %s\n' % (hostname, key, value))
    f.close()
    # os.system('zabbix_sender -z %s -i postgres_log_port_%s.log'% (zabbix_server,port))