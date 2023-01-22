from django.urls import path

from crawler.views import index, start_task, get_task_status


urlpatterns = [
    path('', index, name='index'),
    path('crawlers/', start_task, name='start_task'),
    path('crawlers/<task_id>/', get_task_status, name='get_start_status'),
]