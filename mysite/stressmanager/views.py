from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from stressmanager.alchemytest import checkIn

def index(request):
	context = {'newMessage' : checkIn("I love puppies!"), 'STATIC_URL' : "/static/style.css"}
	return HttpResponse(render(request, 'base.html', context))
