from celery import Celery

app = Celery('app')
app.config_from_object('config.celery_config')
app.autodiscover_tasks(['app.tasks'])

if __name__ == '__main__':
    app.start()