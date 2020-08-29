from django.http import JsonResponse, HttpResponse
import requests

from django.conf import settings


# Create your views here.
def test(request):
    return HttpResponse("Hello World")


def reload(request):
    url = "http://localhost:" + settings.BFE_MONITOR_PORT + "/reload/"
    return JsonResponse(requests.get(url).text)
