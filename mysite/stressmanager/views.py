from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from stressmanager.alchemytest import check_in

def index(request):
	context = {'text1' : 'Hello!', 'text2': 'What\'s on your mind?', 'STATIC_URL' : "/static/style.css"}
	return HttpResponse(render(request, 'input.html', context))

def request_page(request):
	userInput = request.GET.get('mytextarea')
	userName = request.GET.get('username')
	context = {'newMessage' : check_in(userInput, 'history.txt', userName), 'STATIC_URL' : "/static/style.css"}
	return HttpResponse(render(request, 'thanks.html', context))
