if 'Table' not in locals() and 'Table' not in globals():
  from sqlalchemy import Table, Column, Float, Integer, String, MetaData, ForeignKey
  metadata = MetaData()

archived_condor_jobs = Table('archived_condor_jobs', metadata,
  Column('global_job_id', String(128), primary_key=True),
  Column('group_name', String(128)),
  Column('target_clouds', String),
  Column('cloud_name', String),
  Column('job_status', Integer),
  Column('request_cpus', Integer),
  Column('request_ram', Integer),
  Column('request_disk', Integer),
  Column('request_swap', Integer),
  Column('request_scratch', Integer),
  Column('requirements', String(512)),
  Column('job_priority', Integer),
  Column('cluster_id', Integer),
  Column('proc_id', Integer),
  Column('user', String(512)),
  Column('image', String),
  Column('instance_type', String(512)),
  Column('network', String(512)),
  Column('keep_alive', String(512)),
  Column('max_price', String(512)),
  Column('user_data', String(512)),
  Column('job_per_core', Integer),
  Column('entered_current_status', Integer),
  Column('q_date', Integer),
  Column('hold_job_reason', String(64)),
  Column('held_reason', String(64))
  )

archived_condor_machines = Table('archived_condor_machines', metadata,
  Column('name', String(128), primary_key=True),
  Column('machine', String(256)),
  Column('group_name', String(32)),
  Column('condor_host', String(64)),
  Column('flavor', String(32)),
  Column('job_id', String(128)),
  Column('global_job_id', String(128)),
  Column('address', String(512)),
  Column('state', String(128)),
  Column('activity', String(128)),
  Column('vm_type', String(128)),
  Column('my_current_time', Integer),
  Column('entered_current_state', Integer),
  Column('start', String(128)),
  Column('remote_owner', String(128)),
  Column('slot_type', String(128)),
  Column('total_slots', Integer),
  Column('idle_time', Integer),
  Column('retire_request_time', Integer),
  Column('retired_time', Integer)
  )

auth_group = Table('auth_group', metadata,
  Column('id', Integer, primary_key=True),
  Column('name', String(80))
  )

auth_group_permissions = Table('auth_group_permissions', metadata,
  Column('id', Integer, primary_key=True),
  Column('group_id', Integer),
  Column('permission_id', Integer)
  )

auth_permission = Table('auth_permission', metadata,
  Column('id', Integer, primary_key=True),
  Column('name', String(255)),
  Column('content_type_id', Integer),
  Column('codename', String(100))
  )

auth_user = Table('auth_user', metadata,
  Column('id', Integer, primary_key=True),
  Column('password', String(128)),
  Column('last_login', Integer),
  Column('is_superuser', Integer),
  Column('username', String(150)),
  Column('first_name', String(30)),
  Column('last_name', String(150)),
  Column('email', String(254)),
  Column('is_staff', Integer),
  Column('is_active', Integer),
  Column('date_joined', Integer)
  )

auth_user_groups = Table('auth_user_groups', metadata,
  Column('id', Integer, primary_key=True),
  Column('user_id', Integer),
  Column('group_id', Integer)
  )

auth_user_user_permissions = Table('auth_user_user_permissions', metadata,
  Column('id', Integer, primary_key=True),
  Column('user_id', Integer),
  Column('permission_id', Integer)
  )

cloud_flavors = Table('cloud_flavors', metadata,
  Column('group_name', String(32), primary_key=True),
  Column('cloud_name', String(32), primary_key=True),
  Column('id', String(128)),
  Column('ram', Integer),
  Column('cores', Integer),
  Column('swap', Integer),
  Column('disk', Integer),
  Column('ephemeral_disk', Integer),
  Column('is_public', Integer),
  Column('last_updated', Integer),
  Column('name', String(128), primary_key=True)
  )

cloud_images = Table('cloud_images', metadata,
  Column('group_name', String(32), primary_key=True),
  Column('cloud_name', String(32), primary_key=True),
  Column('id', String(128), primary_key=True),
  Column('container_format', String(128)),
  Column('disk_format', String(128)),
  Column('name', String(256)),
  Column('size', Integer),
  Column('visibility', String(128)),
  Column('min_disk', Integer),
  Column('min_ram', Integer),
  Column('last_updated', Integer)
  )

cloud_keypairs = Table('cloud_keypairs', metadata,
  Column('group_name', String(32), primary_key=True),
  Column('cloud_name', String(32), primary_key=True),
  Column('fingerprint', String(64), primary_key=True),
  Column('key_name', String(32), primary_key=True)
  )

cloud_limits = Table('cloud_limits', metadata,
  Column('group_name', String(32), primary_key=True),
  Column('cloud_name', String(32), primary_key=True),
  Column('server_meta_max', Integer),
  Column('instances_max', Integer),
  Column('personality_max', Integer),
  Column('image_meta_max', Integer),
  Column('personality_size_max', Integer),
  Column('ram_max', Integer),
  Column('server_groups_max', Integer),
  Column('security_group_rules_max', Integer),
  Column('keypairs_max', Integer),
  Column('security_groups_max', Integer),
  Column('server_group_members_max', Integer),
  Column('floating_ips_max', Integer),
  Column('cores_max', Integer),
  Column('server_groups_used', Integer),
  Column('instances_used', Integer),
  Column('ram_used', Integer),
  Column('security_groups_used', Integer),
  Column('floating_ips_used', Integer),
  Column('cores_used', Integer),
  Column('last_updated', Integer)
  )

cloud_networks = Table('cloud_networks', metadata,
  Column('group_name', String(32), primary_key=True),
  Column('cloud_name', String(32), primary_key=True),
  Column('id', String(128), primary_key=True),
  Column('name', String(256)),
  Column('subnets', String(256)),
  Column('tenant_id', String(128)),
  Column('external_route', Integer),
  Column('shared', Integer),
  Column('last_updated', Integer)
  )

condor_jobs = Table('condor_jobs', metadata,
  Column('global_job_id', String(128), primary_key=True),
  Column('group_name', String(32)),
  Column('target_clouds', String),
  Column('job_status', Integer),
  Column('request_cpus', Integer),
  Column('request_ram', Integer),
  Column('request_disk', Integer),
  Column('request_swap', Integer),
  Column('request_scratch', Integer),
  Column('requirements', String(512)),
  Column('job_priority', Integer),
  Column('cluster_id', Integer),
  Column('proc_id', Integer),
  Column('user', String(512)),
  Column('image', String),
  Column('instance_type', String(512)),
  Column('network', String(512)),
  Column('keep_alive', String(512)),
  Column('max_price', String(512)),
  Column('user_data', String(512)),
  Column('job_per_core', Integer),
  Column('entered_current_status', Integer),
  Column('q_date', Integer),
  Column('hold_reason_code', Integer),
  Column('hold_reason_subcode', Integer),
  Column('last_remote_host', String(64)),
  Column('held_reason', String(64)),
  Column('hold_job_reason', String(64))
  )

condor_machines = Table('condor_machines', metadata,
  Column('name', String(128), primary_key=True),
  Column('machine', String(256)),
  Column('group_name', String(32)),
  Column('condor_host', String(64)),
  Column('flavor', String(32)),
  Column('job_id', String(128)),
  Column('global_job_id', String(128)),
  Column('address', String(512)),
  Column('state', String(128)),
  Column('activity', String(128)),
  Column('vm_type', String(128)),
  Column('my_current_time', Integer),
  Column('entered_current_state', Integer),
  Column('start', String(128)),
  Column('remote_owner', String(128)),
  Column('slot_type', String(128)),
  Column('slot_cpus', Integer),
  Column('total_slots', Integer),
  Column('idle_time', Integer),
  Column('deprecated-retire_request_time', Integer),
  Column('deprecated-retired_time', Integer)
  )

csv2_attribute_mapping = Table('csv2_attribute_mapping', metadata,
  Column('csv2', String(64), primary_key=True),
  Column('os_limits', String(64)),
  Column('os_flavors', String(64)),
  Column('os_images', String(64)),
  Column('os_networks', String(64)),
  Column('os_vms', String(64)),
  Column('condor', String(64))
  )

csv2_cloud_flavor_exclusions = Table('csv2_cloud_flavor_exclusions', metadata,
  Column('group_name', String(32), primary_key=True),
  Column('cloud_name', String(32), primary_key=True),
  Column('flavor_name', String(128), primary_key=True)
  )

csv2_cloud_metadata = Table('csv2_cloud_metadata', metadata,
  Column('group_name', String(32), primary_key=True),
  Column('cloud_name', String(32), primary_key=True),
  Column('metadata_name', String(64), primary_key=True),
  Column('enabled', Integer),
  Column('priority', Integer),
  Column('metadata', String),
  Column('mime_type', String(128))
  )

csv2_cloud_types = Table('csv2_cloud_types', metadata,
  Column('cloud_type', String(32), primary_key=True)
  )

csv2_clouds = Table('csv2_clouds', metadata,
  Column('group_name', String(32), primary_key=True),
  Column('cloud_name', String(32), primary_key=True),
  Column('enabled', Integer),
  Column('authurl', String(128)),
  Column('project', String(128)),
  Column('username', String(20)),
  Column('password', String),
  Column('keyname', String(20)),
  Column('cacertificate', String),
  Column('region', String(20)),
  Column('user_domain_name', String(20)),
  Column('project_domain_name', String(20)),
  Column('cloud_type', String(64)),
  Column('server_meta_ctl', Integer),
  Column('instances_ctl', Integer),
  Column('personality_ctl', Integer),
  Column('image_meta_ctl', Integer),
  Column('personality_size_ctl', Integer),
  Column('ram_ctl', Integer),
  Column('server_groups_ctl', Integer),
  Column('security_group_rules_ctl', Integer),
  Column('keypairs_ctl', Integer),
  Column('security_groups_ctl', Integer),
  Column('server_group_members_ctl', Integer),
  Column('floating_ips_ctl', Integer),
  Column('cores_ctl', Integer),
  Column('cores_softmax', Integer),
  Column('spot_price', Integer),
  Column('vm_flavor', String(64)),
  Column('vm_image', String(64)),
  Column('vm_keep_alive', Integer),
  Column('vm_keyname', String(64)),
  Column('vm_network', String(64)),
  Column('error_count', Integer),
  Column('error_time', Integer)
  )

csv2_config = Table('csv2_config', metadata,
  Column('config_name', String(64), primary_key=True),
  Column('yaml', String)
  )

csv2_configuration = Table('csv2_configuration', metadata,
  Column('category', String(32), primary_key=True),
  Column('config_key', String(32), primary_key=True),
  Column('config_type', String(16)),
  Column('config_value', String(128))
  )

csv2_group_metadata = Table('csv2_group_metadata', metadata,
  Column('group_name', String(32), primary_key=True),
  Column('metadata_name', String(64), primary_key=True),
  Column('enabled', Integer),
  Column('priority', Integer),
  Column('metadata', String),
  Column('mime_type', String(128))
  )

csv2_group_metadata_exclusions = Table('csv2_group_metadata_exclusions', metadata,
  Column('group_name', String(32), primary_key=True),
  Column('metadata_name', String(64), primary_key=True),
  Column('cloud_name', String(32), primary_key=True)
  )

csv2_groups = Table('csv2_groups', metadata,
  Column('group_name', String(32), primary_key=True),
  Column('htcondor_fqdn', String(128)),
  Column('htcondor_container_hostname', String(128)),
  Column('htcondor_other_submitters', String(128)),
  Column('job_cpus', Integer),
  Column('job_ram', Integer),
  Column('job_disk', Integer),
  Column('job_scratch', Integer),
  Column('job_swap', Integer),
  Column('vm_flavor', String(64)),
  Column('vm_image', String(64)),
  Column('vm_keep_alive', Integer),
  Column('vm_keyname', String(64)),
  Column('vm_network', String(64))
  )

csv2_mime_types = Table('csv2_mime_types', metadata,
  Column('mime_type', String(32), primary_key=True)
  )

csv2_poll_times = Table('csv2_poll_times', metadata,
  Column('process_id', String(64), primary_key=True),
  Column('last_poll', Integer)
  )

csv2_service_catalog = Table('csv2_service_catalog', metadata,
  Column('service', String(64), primary_key=True),
  Column('fqdn', String(128), primary_key=True),
  Column('last_updated', Integer),
  Column('flag_htcondor_allow', Integer),
  Column('yaml_attribute_name', String(64))
  )

csv2_system_status = Table('csv2_system_status', metadata,
  Column('id', Integer, primary_key=True),
  Column('csv2_main_status', Integer),
  Column('csv2_main_msg', String(512)),
  Column('mariadb_status', Integer),
  Column('mariadb_msg', String(512)),
  Column('csv2_openstack_error_count', Integer),
  Column('csv2_openstack_status', Integer),
  Column('csv2_openstack_msg', String(512)),
  Column('csv2_jobs_error_count', Integer),
  Column('csv2_jobs_status', Integer),
  Column('csv2_jobs_msg', String(512)),
  Column('csv2_machines_error_count', Integer),
  Column('csv2_machines_status', Integer),
  Column('csv2_machines_msg', String(512)),
  Column('condor_status', Integer),
  Column('condor_msg', String(512)),
  Column('load', Float),
  Column('ram', Float),
  Column('ram_size', Float),
  Column('ram_used', Float),
  Column('swap', Float),
  Column('swap_size', Float),
  Column('swap_used', Float),
  Column('disk', Float),
  Column('disk_size', Float),
  Column('disk_used', Float)
  )

csv2_user = Table('csv2_user', metadata,
  Column('username', String(32), primary_key=True),
  Column('cert_cn', String(128)),
  Column('password', String(128)),
  Column('is_superuser', Integer),
  Column('join_date', Integer),
  Column('active_group', String(128)),
  Column('flag_global_status', Integer),
  Column('status_refresh_interval', Integer)
  )

csv2_user_groups = Table('csv2_user_groups', metadata,
  Column('username', String(32), primary_key=True),
  Column('group_name', String(32), primary_key=True)
  )

csv2_vms = Table('csv2_vms', metadata,
  Column('group_name', String(32), primary_key=True),
  Column('cloud_name', String(32), primary_key=True),
  Column('vmid', String(128), primary_key=True),
  Column('vm_ips', String(128)),
  Column('vm_floating_ips', String(128)),
  Column('auth_url', String(128)),
  Column('project', String(128)),
  Column('hostname', String(128)),
  Column('keep_alive', Integer),
  Column('start_time', Integer),
  Column('status', String(32)),
  Column('flavor_id', String(128)),
  Column('task', String(32)),
  Column('power_status', Integer),
  Column('manual_control', Integer),
  Column('htcondor_partitionable_slots', Integer),
  Column('htcondor_dynamic_slots', Integer),
  Column('htcondor_slots_timestamp', Integer),
  Column('retire', Integer),
  Column('retire_time', Integer),
  Column('terminate', Integer),
  Column('terminate_time', Integer),
  Column('status_changed_time', Integer),
  Column('last_updated', Integer)
  )

csv2_vms_foreign = Table('csv2_vms_foreign', metadata,
  Column('group_name', String(32), primary_key=True),
  Column('cloud_name', String(32), primary_key=True),
  Column('flavor_id', String(128), primary_key=True),
  Column('count', Integer)
  )

django_admin_log = Table('django_admin_log', metadata,
  Column('id', Integer, primary_key=True),
  Column('action_time', Integer),
  Column('object_id', String),
  Column('object_repr', String(200)),
  Column('action_flag', Integer),
  Column('change_message', String),
  Column('content_type_id', Integer),
  Column('user_id', Integer)
  )

django_content_type = Table('django_content_type', metadata,
  Column('id', Integer, primary_key=True),
  Column('app_label', String(100)),
  Column('model', String(100))
  )

django_migrations = Table('django_migrations', metadata,
  Column('id', Integer, primary_key=True),
  Column('app', String(255)),
  Column('name', String(255)),
  Column('applied', Integer)
  )

django_session = Table('django_session', metadata,
  Column('session_key', String(40), primary_key=True),
  Column('session_data', String),
  Column('expire_date', Integer)
  )

silk_profile = Table('silk_profile', metadata,
  Column('id', Integer, primary_key=True),
  Column('name', String(300)),
  Column('start_time', Integer),
  Column('end_time', Integer),
  Column('time_taken', Float),
  Column('file_path', String(300)),
  Column('line_num', Integer),
  Column('end_line_num', Integer),
  Column('func_name', String(300)),
  Column('exception_raised', Integer),
  Column('dynamic', Integer),
  Column('request_id', String(36))
  )

silk_profile_queries = Table('silk_profile_queries', metadata,
  Column('id', Integer, primary_key=True),
  Column('profile_id', Integer),
  Column('sqlquery_id', Integer)
  )

silk_request = Table('silk_request', metadata,
  Column('id', String(36), primary_key=True),
  Column('path', String(190)),
  Column('query_params', String),
  Column('raw_body', String),
  Column('body', String),
  Column('method', String(10)),
  Column('start_time', Integer),
  Column('view_name', String(190)),
  Column('end_time', Integer),
  Column('time_taken', Float),
  Column('encoded_headers', String),
  Column('meta_time', Float),
  Column('meta_num_queries', Integer),
  Column('meta_time_spent_queries', Float),
  Column('pyprofile', String),
  Column('num_sql_queries', Integer),
  Column('prof_file', String(300))
  )

silk_response = Table('silk_response', metadata,
  Column('id', String(36), primary_key=True),
  Column('status_code', Integer),
  Column('raw_body', String),
  Column('body', String),
  Column('encoded_headers', String),
  Column('request_id', String(36))
  )

silk_sqlquery = Table('silk_sqlquery', metadata,
  Column('id', Integer, primary_key=True),
  Column('query', String),
  Column('start_time', Integer),
  Column('end_time', Integer),
  Column('time_taken', Float),
  Column('traceback', String),
  Column('request_id', String(36))
  )

test_table = Table('test_table', metadata,
  Column('hostname', String(128), primary_key=True),
  Column('htcondor_dynamic_slots', Integer),
  Column('htcondor_dynamic_slots_changed', Integer)
  )

view_available_resources = Table('view_available_resources', metadata,
  Column('group_name', String(32)),
  Column('cloud_name', String(32)),
  Column('region', String(20)),
  Column('cloud_type', String(64)),
  Column('spot_price', Integer),
  Column('authurl', String(128)),
  Column('cacertificate', String),
  Column('project_domain_name', String(20)),
  Column('project', String(128)),
  Column('user_domain_name', String(20)),
  Column('username', String(20)),
  Column('password', String),
  Column('default_flavor', String(97)),
  Column('default_image', String(64)),
  Column('default_keep_alive', Integer),
  Column('default_keyname', String(64)),
  Column('default_network', String(64)),
  Column('VMs', Integer),
  Column('cores_max', Integer),
  Column('cores_used', Integer),
  Column('disk_used', Integer),
  Column('ram_max', Integer),
  Column('ram_used', Integer),
  Column('swap_used', Integer),
  Column('flavor', String(161)),
  Column('flavor_id', String(128)),
  Column('flavor_slots', Integer),
  Column('flavor_cores', Integer),
  Column('flavor_disk', Integer),
  Column('flavor_ram', Integer),
  Column('flavor_swap', Integer),
  Column('flavor_VMs', Integer),
  Column('flavor_manual', Integer),
  Column('flavor_error', Integer),
  Column('flavor_retiring', Integer)
  )

view_cloud_status = Table('view_cloud_status', metadata,
  Column('group_name', String(32)),
  Column('cloud_name', String(32)),
  Column('VMs', Integer),
  Column('VMs_manual', Integer),
  Column('VMs_in_error', Integer),
  Column('VMs_starting', Integer),
  Column('VMs_retiring', Integer),
  Column('VMs_unregistered', Integer),
  Column('VMs_idle', Integer),
  Column('VMs_running', Integer),
  Column('cores_native', Integer),
  Column('ram_native', Integer),
  Column('slot_count', Integer),
  Column('slot_core_count', Integer),
  Column('slot_idle_core_count', Integer),
  Column('Foreign_VMs', Integer),
  Column('enabled', Integer),
  Column('cores_ctl', Integer),
  Column('cores_limit', Integer),
  Column('cores_quota', Integer),
  Column('cores_foreign', Integer),
  Column('cores_native_foreign', Integer),
  Column('ram_ctl', Integer),
  Column('ram_limit', Integer),
  Column('ram_quota', Integer),
  Column('ram_foreign', Integer),
  Column('ram_native_foreign', Integer)
  )

view_cloud_status_slot_detail = Table('view_cloud_status_slot_detail', metadata,
  Column('group_name', String(256)),
  Column('cloud_name', String(256)),
  Column('slot_tag', String(392)),
  Column('slot_id', String(380)),
  Column('slot_type', Integer),
  Column('slot_count', Integer),
  Column('core_count', Integer)
  )

view_clouds = Table('view_clouds', metadata,
  Column('group_name', String(32)),
  Column('cloud_name', String(32)),
  Column('enabled', Integer),
  Column('spot_price', Integer),
  Column('vm_flavor', String(64)),
  Column('vm_image', String(64)),
  Column('vm_keep_alive', Integer),
  Column('vm_keyname', String(64)),
  Column('vm_network', String(64)),
  Column('cascading_vm_flavor', String(64)),
  Column('cascading_vm_image', String(64)),
  Column('cascading_vm_keep_alive', Integer),
  Column('cascading_vm_keyname', String(64)),
  Column('cascading_vm_network', String(64)),
  Column('authurl', String(128)),
  Column('project_domain_name', String(20)),
  Column('project', String(128)),
  Column('user_domain_name', String(20)),
  Column('username', String(20)),
  Column('password', String),
  Column('keyname', String(20)),
  Column('cacertificate', String),
  Column('region', String(20)),
  Column('cloud_type', String(64)),
  Column('cores_ctl', Integer),
  Column('cores_softmax', Integer),
  Column('cores_max', Integer),
  Column('cores_used', Integer),
  Column('cores_foreign', Integer),
  Column('cores_native', Integer),
  Column('ram_ctl', Integer),
  Column('ram_max', Integer),
  Column('ram_used', Integer),
  Column('ram_foreign', Integer),
  Column('ram_native', Integer),
  Column('instances_max', Integer),
  Column('instances_used', Integer),
  Column('floating_ips_max', Integer),
  Column('floating_ips_used', Integer),
  Column('security_groups_max', Integer),
  Column('security_groups_used', Integer),
  Column('server_groups_max', Integer),
  Column('server_groups_used', Integer),
  Column('image_meta_max', Integer),
  Column('keypairs_max', Integer),
  Column('personality_max', Integer),
  Column('personality_size_max', Integer),
  Column('security_group_rules_max', Integer),
  Column('server_group_members_max', Integer),
  Column('server_meta_max', Integer),
  Column('cores_idle', Integer),
  Column('ram_idle', Integer)
  )

view_clouds_with_metadata_info = Table('view_clouds_with_metadata_info', metadata,
  Column('group_name', String(32)),
  Column('cloud_name', String(32)),
  Column('enabled', Integer),
  Column('spot_price', Integer),
  Column('vm_flavor', String(64)),
  Column('vm_image', String(64)),
  Column('vm_keep_alive', Integer),
  Column('vm_keyname', String(64)),
  Column('vm_network', String(64)),
  Column('cascading_vm_flavor', String(64)),
  Column('cascading_vm_image', String(64)),
  Column('cascading_vm_keep_alive', Integer),
  Column('cascading_vm_keyname', String(64)),
  Column('cascading_vm_network', String(64)),
  Column('authurl', String(128)),
  Column('project_domain_name', String(20)),
  Column('project', String(128)),
  Column('user_domain_name', String(20)),
  Column('username', String(20)),
  Column('password', String),
  Column('keyname', String(20)),
  Column('cacertificate', String),
  Column('region', String(20)),
  Column('cloud_type', String(64)),
  Column('cores_ctl', Integer),
  Column('cores_softmax', Integer),
  Column('cores_max', Integer),
  Column('cores_used', Integer),
  Column('cores_foreign', Integer),
  Column('cores_native', Integer),
  Column('ram_ctl', Integer),
  Column('ram_max', Integer),
  Column('ram_used', Integer),
  Column('ram_foreign', Integer),
  Column('ram_native', Integer),
  Column('instances_max', Integer),
  Column('instances_used', Integer),
  Column('floating_ips_max', Integer),
  Column('floating_ips_used', Integer),
  Column('security_groups_max', Integer),
  Column('security_groups_used', Integer),
  Column('server_groups_max', Integer),
  Column('server_groups_used', Integer),
  Column('image_meta_max', Integer),
  Column('keypairs_max', Integer),
  Column('personality_max', Integer),
  Column('personality_size_max', Integer),
  Column('security_group_rules_max', Integer),
  Column('server_group_members_max', Integer),
  Column('server_meta_max', Integer),
  Column('cores_idle', Integer),
  Column('ram_idle', Integer),
  Column('metadata_name', String(64)),
  Column('metadata_enabled', Integer),
  Column('metadata_priority', Integer),
  Column('metadata_mime_type', String(128))
  )

view_clouds_with_metadata_names = Table('view_clouds_with_metadata_names', metadata,
  Column('group_name', String(32)),
  Column('cloud_name', String(32)),
  Column('enabled', Integer),
  Column('spot_price', Integer),
  Column('vm_flavor', String(64)),
  Column('vm_image', String(64)),
  Column('vm_keep_alive', Integer),
  Column('vm_keyname', String(64)),
  Column('vm_network', String(64)),
  Column('cascading_vm_flavor', String(64)),
  Column('cascading_vm_image', String(64)),
  Column('cascading_vm_keep_alive', Integer),
  Column('cascading_vm_keyname', String(64)),
  Column('cascading_vm_network', String(64)),
  Column('authurl', String(128)),
  Column('project_domain_name', String(20)),
  Column('project', String(128)),
  Column('user_domain_name', String(20)),
  Column('username', String(20)),
  Column('password', String),
  Column('keyname', String(20)),
  Column('cacertificate', String),
  Column('region', String(20)),
  Column('cloud_type', String(64)),
  Column('cores_ctl', Integer),
  Column('cores_softmax', Integer),
  Column('cores_max', Integer),
  Column('cores_used', Integer),
  Column('cores_foreign', Integer),
  Column('cores_native', Integer),
  Column('ram_ctl', Integer),
  Column('ram_max', Integer),
  Column('ram_used', Integer),
  Column('ram_foreign', Integer),
  Column('ram_native', Integer),
  Column('instances_max', Integer),
  Column('instances_used', Integer),
  Column('floating_ips_max', Integer),
  Column('floating_ips_used', Integer),
  Column('security_groups_max', Integer),
  Column('security_groups_used', Integer),
  Column('server_groups_max', Integer),
  Column('server_groups_used', Integer),
  Column('image_meta_max', Integer),
  Column('keypairs_max', Integer),
  Column('personality_max', Integer),
  Column('personality_size_max', Integer),
  Column('security_group_rules_max', Integer),
  Column('server_group_members_max', Integer),
  Column('server_meta_max', Integer),
  Column('cores_idle', Integer),
  Column('ram_idle', Integer),
  Column('flavor_exclusions', String),
  Column('flavor_names', String),
  Column('group_exclusions', String),
  Column('metadata_names', String)
  )

view_condor_host = Table('view_condor_host', metadata,
  Column('group_name', String(32)),
  Column('cloud_name', String(32)),
  Column('htcondor_fqdn', String(128)),
  Column('vmid', String(128)),
  Column('hostname', String(128)),
  Column('retire', Integer),
  Column('terminate', Integer),
  Column('machine', String(256))
  )

view_condor_jobs_group_defaults_applied = Table('view_condor_jobs_group_defaults_applied', metadata,
  Column('global_job_id', String(128)),
  Column('group_name', String(32)),
  Column('target_clouds', String),
  Column('job_status', Integer),
  Column('request_cpus', Integer),
  Column('request_disk', Integer),
  Column('request_ram', Integer),
  Column('request_swap', Integer),
  Column('requirements', String(512)),
  Column('job_priority', Integer),
  Column('cluster_id', Integer),
  Column('proc_id', Integer),
  Column('user', String(512)),
  Column('image', String),
  Column('instance_type', String(512)),
  Column('network', String(512)),
  Column('keep_alive', String(512)),
  Column('max_price', String(512)),
  Column('user_data', String(512)),
  Column('job_per_core', Integer),
  Column('entered_current_status', Integer),
  Column('q_date', Integer),
  Column('hold_job_reason', String(64)),
  Column('held_reason', String(64)),
  Column('js_idle', Integer),
  Column('js_running', Integer),
  Column('js_completed', Integer),
  Column('js_held', Integer),
  Column('js_other', Integer)
  )

view_groups_of_idle_jobs = Table('view_groups_of_idle_jobs', metadata,
  Column('group_name', String(32)),
  Column('target_clouds', String),
  Column('instance_type', String(512)),
  Column('requirements', String(512)),
  Column('job_priority', Integer),
  Column('user', String(512)),
  Column('image', String),
  Column('network', String(512)),
  Column('keep_alive', String(512)),
  Column('max_price', String(512)),
  Column('user_data', String(512)),
  Column('job_per_core', Integer),
  Column('request_cpus_min', Integer),
  Column('request_cpus_max', Integer),
  Column('request_cpus_total', Integer),
  Column('request_disk_min', Integer),
  Column('request_disk_max', Integer),
  Column('request_disk_total', Integer),
  Column('request_ram_min', Integer),
  Column('request_ram_max', Integer),
  Column('request_ram_total', Integer),
  Column('request_swap_min', Integer),
  Column('request_swap_max', Integer),
  Column('request_swap_total', Integer),
  Column('queue_date', Integer),
  Column('idle', Integer),
  Column('running', Integer),
  Column('completed', Integer),
  Column('held', Integer),
  Column('other', Integer),
  Column('flavors', String)
  )

view_groups_with_metadata_info = Table('view_groups_with_metadata_info', metadata,
  Column('group_name', String(32)),
  Column('htcondor_fqdn', String(128)),
  Column('htcondor_container_hostname', String(128)),
  Column('htcondor_other_submitters', String(128)),
  Column('metadata_name', String(64)),
  Column('metadata_enabled', Integer),
  Column('metadata_priority', Integer),
  Column('metadata_mime_type', String(128))
  )

view_groups_with_metadata_names = Table('view_groups_with_metadata_names', metadata,
  Column('group_name', String(32)),
  Column('htcondor_fqdn', String(128)),
  Column('htcondor_container_hostname', String(128)),
  Column('htcondor_other_submitters', String(128)),
  Column('metadata_names', String)
  )

view_idle_vms = Table('view_idle_vms', metadata,
  Column('group_name', String(32)),
  Column('cloud_name', String(32)),
  Column('keep_alive', Integer),
  Column('vmid', String(128)),
  Column('machine', String(256)),
  Column('claimed', Integer),
  Column('retire', Integer),
  Column('terminate', Integer),
  Column('age', Float)
  )

view_job_status = Table('view_job_status', metadata,
  Column('group_name', String(32)),
  Column('Jobs', Integer),
  Column('Idle', Integer),
  Column('Running', Integer),
  Column('Completed', Integer),
  Column('Held', Integer),
  Column('Other', Integer)
  )

view_metadata_collation = Table('view_metadata_collation', metadata,
  Column('group_name', String(32)),
  Column('cloud_name', String(32)),
  Column('type', String(5)),
  Column('priority', Integer),
  Column('metadata_name', String(64)),
  Column('mime_type', String(128))
  )

view_metadata_collation_json = Table('view_metadata_collation_json', metadata,
  Column('group_metadata', String)
  )

view_redundant_machines = Table('view_redundant_machines', metadata,
  Column('group_name', String(32)),
  Column('hostname', String(256)),
  Column('condor_host', String(64)),
  Column('name', String(128)),
  Column('entered_current_state', Integer),
  Column('cloud_name', String(32))
  )

view_user_groups = Table('view_user_groups', metadata,
  Column('username', String(32)),
  Column('cert_cn', String(128)),
  Column('password', String(128)),
  Column('is_superuser', Integer),
  Column('join_date', Integer),
  Column('active_group', String(128)),
  Column('user_groups', String),
  Column('available_groups', String)
  )

view_user_groups_available = Table('view_user_groups_available', metadata,
  Column('username', String(32)),
  Column('group_name', String(32)),
  Column('available', String(32))
  )

view_vm_kill_retire_priority_age = Table('view_vm_kill_retire_priority_age', metadata,
  Column('group_name', String(32)),
  Column('cloud_name', String(32)),
  Column('vmid', String(128)),
  Column('flavor_id', String(128)),
  Column('machine', String(256)),
  Column('killed', Integer),
  Column('retired', Integer),
  Column('priority', Integer),
  Column('flavor_cores', Integer),
  Column('flavor_ram', Integer)
  )

view_vm_kill_retire_priority_idle = Table('view_vm_kill_retire_priority_idle', metadata,
  Column('group_name', String(32)),
  Column('cloud_name', String(32)),
  Column('vmid', String(128)),
  Column('machine', String(256)),
  Column('killed', Integer),
  Column('retired', Integer),
  Column('priority', Integer)
  )

view_vms = Table('view_vms', metadata,
  Column('group_name', String(32)),
  Column('cloud_name', String(32)),
  Column('vmid', String(128)),
  Column('vm_ips', String(128)),
  Column('vm_floating_ips', String(128)),
  Column('auth_url', String(128)),
  Column('project', String(128)),
  Column('hostname', String(128)),
  Column('keep_alive', Integer),
  Column('start_time', Integer),
  Column('status', String(32)),
  Column('flavor_id', String(128)),
  Column('task', String(32)),
  Column('power_status', Integer),
  Column('manual_control', Integer),
  Column('retire', Integer),
  Column('retire_time', Integer),
  Column('terminate', Integer),
  Column('terminate_time', Integer),
  Column('status_changed_time', Integer),
  Column('last_updated', Integer),
  Column('flavor_name', String(128)),
  Column('condor_slots', Integer),
  Column('condor_slots_used', Integer),
  Column('machine', String(256)),
  Column('my_current_time', Integer),
  Column('entered_current_state', Integer),
  Column('idle_time', Integer),
  Column('foreign_vm', Integer),
  Column('cores', Integer),
  Column('disk', Integer),
  Column('ram', Integer),
  Column('swap', Integer),
  Column('poller_status', String(12))
  )

xxx = Table('xxx', metadata,
  Column('machine', String(256)),
  Column('changed', Integer)
  )

yyy = Table('yyy', metadata,
  Column('machine', String(256)),
  Column('changed', Integer)
  )

