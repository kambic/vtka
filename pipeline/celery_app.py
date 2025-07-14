from celery import Celery

app = Celery("vod_pipeline")
app.config_from_object("vod_pipeline.config")
app.autodiscover_tasks(["vod_pipeline.tasks"])
