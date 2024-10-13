import os

wsgi_app = "ibks_twitter.wsgi:application"
loglevel = "warning"

cpu_cnt = os.cpu_count()
if cpu_cnt != None:
    workers = 2 * cpu_cnt
else:
    workers = 2

bind = "0.0.0.0:8000"

# Restart workers when code changes (True for development only!)
reload = False

# Write access and error info to /var/log
accesslog = errorlog = "/var/log/gunicorn/gunicorn.log"

# Redirect stdout/stderr to log file
capture_output = True

# PID file so you can easily fetch process ID
pidfile = "/var/run/gunicorn/gunicorn.pid"

# Daemonize the Gunicorn process (detach & enter background)
daemon = True
