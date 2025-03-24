import os
from celery import Celery

# 設定 Django settings 模組
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'factory_project.settings')

app = Celery('factory_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# 測試任務（可略）
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
