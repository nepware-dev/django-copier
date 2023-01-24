import functools
import os

from celery import Celery
from django.core.cache import cache

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{ project_name }}.settings')

app = Celery('{{ project_name }}')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
def no_simultaneous_execution(f):
    @functools.wraps(f)
    def wrapper(self, *args, **kwargs):
        cache_key = f"running-task-{self.name}-{self.request.id}"
        if not cache.get(cache_key):
            cache.set(cache_key, "lock", timeout=None)
            try:
                f(self, *args, **kwargs)
            except Exception as err:
                cache.delete(cache_key)
                raise err
            finally:
                cache.delete(cache_key)

    return wrapper