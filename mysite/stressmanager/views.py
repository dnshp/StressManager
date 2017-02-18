from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

def index(request):
	context = {'newMessage' : 'Blue', 'STATIC_URL' : settings.STATIC_URL + "style.css"}
	return HttpResponse(render(request, 'base.html', context))
