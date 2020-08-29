from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, Http404
from tokens.models import *


@require_http_methods(['GET'])
def index(request):
    token = request.GET.get('token')
    try:
        t = Token.objects.get(TokenId=token, Enabled=True)
        response = HttpResponse(t.BfeConfig.ZipFile, content_type="application/x-zip-compressed")
        response['Content-Disposition'] = 'inline; filename=' + token + ".zip"
        return response
    except:
        raise Http404
