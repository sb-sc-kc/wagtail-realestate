import os
bind = '0.0.0.0:8080'
workers = 3
backlog = 2048
worker_class = "sync"
debug = True
proc_name = 'gunicorn.proc'
pidfile = '/tmp/gunicorn.pid'
logfile = '/var/log/gunicorn/debug.log'
loglevel = 'WARNING'
