from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger

# Create your views here.

def crawl(request):
	url = request.POST.get('url')
	depth = request.POST.get('depth', 100)
	proxies = request.POST.get('proxies', None)
	proxyhost = request.POST.get('proxyhost', None)
	proxyuser = request.POST.get('proxyuser', None)
	proxypassword = request.POST.get('proxypassword', None)
	proxyport = request.POST.get('proxyport', None)
	proxysecure = request.POST.get('proxysecure', 'http')
	result = ht.getModule('ht_spider').crawl( url=url, depth=depth, proxies=proxies, proxyhost=proxyhost, proxyuser=proxyuser, proxypassword=proxypassword, proxyport=proxyport, proxysecure=proxysecure )
	return renderMainPanel(request=request, popup_text=result)
	