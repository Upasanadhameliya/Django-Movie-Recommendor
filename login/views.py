from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User,auth
from django.contrib import messages
# Create your views here.

def login_page(request):
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['pass']

		try:
			user = User.objects.get(email=email)
		except User.DoesNotExist:
			messages.info(request,'Invalid email!')
			return redirect('/')

		userauth = auth.authenticate(username=user.username,password=password)

		if userauth is not None:
			auth.login(request,user)
			request.session['username'] = user.username
			return redirect('/home/')
		else:
			messages.info(request,'Invalid password!')
			return redirect('/')

	else:
		template = loader.get_template('login/index.html')
		context = {}
		return HttpResponse(template.render(context,request))
