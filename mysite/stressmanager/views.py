from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

def index(request):
	context = {'newMessage' : 'Hello!', 'STATIC_URL' : "/static/style.css"}
	return HttpResponse(render(request, 'base.html', context))
