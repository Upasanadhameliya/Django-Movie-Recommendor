from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.
def registration_page(request):
	if request.method == 'POST':
		username = request.POST['name']
		email = request.POST['email']
		password = request.POST['password']
		passbool = False
		if(password):
			passbool = True
			if len(password) < 8:
				passbool = False
			elif len(password) > 20:
				passbook = False


		if(username and email and passbool):
			if User.objects.filter(username=username).exists():
				messages.info(request,'Username already taken!')
				return redirect('/registration/')
			elif User.objects.filter(email=email).exists():
				messages.info(request,'Email already taken!')
				return redirect('/registration/')
			else:
				new_usr = User(username=username,email=email)
				new_usr.set_password(password)
				new_usr.save()
				return redirect('/')
		elif not passbool:
			messages.info(request,'Password length should be between 8-20 characters!')
			return redirect('/registration/')
		else:
			messages.info(request,'All fields mandatory!')
			return redirect('/registration/')
	else:
		templates = loader.get_template('registration/index.html')
		context = {}
		return HttpResponse(templates.render(context,request))
