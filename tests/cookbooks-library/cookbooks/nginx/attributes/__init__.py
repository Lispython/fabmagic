some_var = "some value"
another_var = "another value"


version = "1.0.12"
url = "http://nginx.org/download/nginx-{0}.tar.gz".format(version)


if system['platform'] in ["debian","ubuntu"]:
    dir        = "/etc/nginx"
    log_dir    = "/var/log/nginx"
    user       = "www-data"
    binary     = "/usr/sbin/nginx"
    init_style = "runit"
else:
    dir        = "/etc/nginx"
    log_dir    = "/var/log/nginx"
    user       = "www-data"
    binary     = "/usr/sbin/nginx"
    init_style = "init"


pid = "/var/run/nginx.pid"

gzip              = "on"
gzip_http_version = "1.0"
gzip_comp_level   = "2"
gzip_proxied      = "any"
gzip_types        = [
    "text/plain",
    "text/html",
    "text/css",
    "application/x-javascript",
    "text/xml",
    "application/xml",
    "application/xml+rss",
    "text/javascript",
    "application/javascript",
    "application/json"]

keepalive          = "on"
keepalive_timeout  = 65
worker_processes   = system['cpu']['total']
worker_connections = 2048
server_names_hash_bucket_size = 64

disable_access_log = False
