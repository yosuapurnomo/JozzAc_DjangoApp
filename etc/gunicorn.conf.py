workers = 3
syslog = True
umask = 0
errorlog = '/root/demo/var/logs/jozzAc.gunicorn.error'
accesslog = '/root/demo/var/logs/jozzAc.gunicorn.access'
loglevel = "info"
user="root"
group="root"

bind = ['101.50.2.224:9001']