wsgi_app = "kvisualbot.wsgi"

worker_class = "gevent"
workers = 1

timeout = 30
graceful_timeout = 10
keepalive = 65

errorlog = "-"
accesslog = "-"
loglevel = "debug"
capture_output = True

forwarded_allow_ips = "*"
proxy_allow_ips = "*"
