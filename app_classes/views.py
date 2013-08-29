
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import addClassForm
from app_classes.models import SectionForm
from django.shortcuts import render
from app_auth.models import UserProfile
from django.contrib.auth.decorators import login_required

from app_classes.forms import addClassForm

@login_required(redirect_field_name='', login_url='/')
def dashboard(request):
	avatar = UserProfile.objects.get(pk = request.user.id).avatar
	return render(request, 'app_classes/dashboard.html', {'avatar':avatar, 'active_nav':'DASHBOARD'})
	
def add_class(request):
	avatar = UserProfile.objects.get(pk = request.user.id).avatar
	return render(request, 'app_classes/add_class.html', {'avatar':avatar})
	
def class_list(request):
	avatar = UserProfile.objects.get(pk = request.user.id).avatar
	return render(request, 'app_classes/dashboard2.html', {'avatar': avatar})

@login_required(redirect_field_name='', login_url='/')
def class_teacher(request):
	avatar = UserProfile.objects.get(pk = request.user.id).avatar
	return render(request, 'app_classes/class_teacher.html', {'avatar':avatar, 'active_nav':'CLASSES'})

@login_required(redirect_field_name='', login_url='/')
def teacher_addNewClass(request):
	avatar = UserProfile.objects.get(pk = request.user.id).avatar
	addClass_form = addClassForm()
	return render(request, 'app_classes/teacher_addNewClass.html', 
			{'addClassForm' : addClass_form, 'next_url': '/classes', 'avatar':avatar, 'active_nav':'CLASSES'})

@login_required(redirect_field_name='', login_url='/')
def submit(request):
	if request.method == "POST":
		form_class = SectionForm(data=request.POST)
		success_url = request.POST.get("next_url", "/")
		if form_class.is_valid():
			form_class.save()
			return redirect(success_url)
		else:
			return render(request, 'app_classes/teacher_addNewClass.html',
				{'addClassForm' : addClassForm, 'next_url': '/class_teacher'})