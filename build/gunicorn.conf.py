workers = 2
bind = "0.0.0.0:1337"
loglevel = "info"
capture_output = True
accesslog = "/app/logs/gunicorn_access.log"
errorlog = "/app/logs/gunicorn_error.log"
