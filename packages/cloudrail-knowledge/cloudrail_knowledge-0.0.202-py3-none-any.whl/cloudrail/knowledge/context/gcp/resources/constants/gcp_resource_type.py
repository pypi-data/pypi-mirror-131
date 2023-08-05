from enum import Enum


class GcpResourceType(Enum):
    NONE = 'none'
    GOOGLE_SQL_DATABASE_INSTANCE = 'google_sql_database_instance'
    GOOGLE_COMPUTE_INSTANCE = 'google_compute_instance'
    GOOGLE_COMPUTE_HEALTH_CHECK = 'google_compute_health_check'
    GOOGLE_COMPUTE_FIREWALL = 'google_compute_firewall'
    GOOGLE_COMPUTE_NETWORK = 'google_compute_network'
    GOOGLE_COMPUTE_SUBNETWORK = 'google_compute_subnetwork'
    GOOGLE_PROJECT = 'google_project'
    GOOGLE_CONTAINER_CLUSTER = 'google_container_cluster'
    GOOGLE_COMPUTE_TARGET_HTTP_PROXY = 'google_compute_target_http_proxy'
    GOOGLE_COMPUTE_TARGET_SSL_PROXY = 'google_compute_target_ssl_proxy'
    GOOGLE_COMPUTE_TARGET_HTTPS_PROXY = 'google_compute_target_https_proxy'
    GOOGLE_COMPUTE_GLOBAL_FORWARDING_RULE = 'google_compute_global_forwarding_rule'
    GOOGLE_COMPUTE_TARGET_POOL = 'google_compute_target_pool'
    GOOGLE_COMPUTE_FORWARDING_RULE = 'google_compute_forwarding_rule'
    GOOGLE_COMPUTE_SSL_POLICY = 'google_compute_ssl_policy'
    GOOGLE_STORAGE_BUCKET = 'google_storage_bucket'
    GOOGLE_DNS_MANAGED_ZONE = 'google_dns_managed_zone'
