from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from stressmanager.alchemytest import check_in

def index(request):
	context = {'newMessage' : check_in("A really cute puppy walked into my lab today, and it totally made up for my bad grade on the midterm!", "history.txt"), 'STATIC_URL' : "/static/style.css"}
	return HttpResponse(render(request, 'base.html', context))
