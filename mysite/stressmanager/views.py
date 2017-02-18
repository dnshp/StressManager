from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from stressmanager.alchemytest import check_in

def index(request):
	context = {'newMessage' : 'Hello!', 'STATIC_URL' : "/static/style.css"}
	return HttpResponse(render(request, 'base.html', context))

def request_page(request):
	if request.GET.get('mybtn'):
		print("CLICK!")
		userInput = request.GET.get('mytextarea')
		context = {'newMessage' : check_in(userInput, 'history.txt'), 'STATIC_URL' : "/static/style.css"}
	return HttpResponse(render(request, 'base.html', context))
