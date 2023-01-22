from celery.result import AsyncResult
from celery.states import FAILURE
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


from crawler.tasks import create_crawling_task


def index(request):
   return render(request, "index.html")


@csrf_exempt
def start_task(request):
    if request.POST:
        url = request.POST.get("url")
        task = create_crawling_task.delay(url)
        return JsonResponse({"task_id": task.id}, status=202)


@csrf_exempt
def get_task_status(request, task_id):

    task_result = AsyncResult(task_id)

    if task_result.status == FAILURE:
        result = []
    else:
        result = task_result.result

    return JsonResponse(
        {
            "task_id": task_id,
            "task_status": task_result.status,
            "task_result": result
        },
        status=200,
    )
