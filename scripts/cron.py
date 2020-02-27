from crontab import CronTab

cron = CronTab(user='admin')
job = cron.new(command='python manage.py runscript hockeyclient')
job.hour.every(6)

job.enable()

cron.write()
