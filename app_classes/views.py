
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from app_classes.models import SectionForm, Section
from django.shortcuts import render
from app_auth.models import UserProfile
from django.db.models import Count, F
from django.contrib.auth.decorators import login_required

from app_classes.forms import addClassForm

@login_required(redirect_field_name='', login_url='/')
def dashboard(request):
	avatar = UserProfile.objects.get(user_id = request.user.id).avatar
	return render(request, 'app_classes/dashboard2.html', {'avatar':avatar, 'active_nav':'DASHBOARD'})
	
def add_class(request):
	avatar = UserProfile.objects.get(user_id = request.user.id).avatar
	return render(request, 'app_classes/add_class.html', {'avatar':avatar})
	
def class_list(request):
	avatar = UserProfile.objects.get(user_id = request.user.id).avatar
	return render(request, 'app_classes/dashboard2.html', {'avatar': avatar})

@login_required(redirect_field_name='', login_url='/')
def class_teacher(request):
	sections = Section.objects.select_related('school__short_name','section_name')
	avatar = UserProfile.objects.get(user_id = request.user.id).avatar
	return render(request, 'app_classes/class_teacher.html', {'avatar':avatar, 'active_nav':'CLASSES', 'sections':sections})

@login_required(redirect_field_name='', login_url='/')
def teacher_addNewClass(request, add_form=None):
	avatar = UserProfile.objects.get(user_id = request.user.id).avatar
	addClass_form = add_form or addClassForm()
	return render(request, 'app_classes/teacher_addNewClass.html', 
			{'addClassForm' : addClass_form, 'next_url': '/classes', 'avatar':avatar, 'active_nav':'CLASSES'})

@login_required(redirect_field_name='', login_url='/')
def submit(request):
	if request.method == "POST":
		form_class = addClassForm(data=request.POST)
		success_url = request.POST.get("next_url", "/")
		if form_class.is_valid():
			form_class = SectionForm(data=request.POST)
			form_class.save()
			return redirect(success_url)
		else:
			return teacher_addNewClass(request, form_class)
<<<<<<< HEAD

@login_required(redirect_field_name='', login_url='/')
def edit(request):
	avatar = UserProfile.objects.get(user_id = request.user.id).avatar
	return render(request, 'app_classes/teacher_editClass.html', {'avatar':avatar, 'active_nav':'CLASSES'})
=======
			
@login_required(redirect_field_name='', login_url='/')
def manualChecking(request):
	sections = Section.objects.annotate(number_of_entries=Count('section_name')).select_related('school__short_name','section_name')
	avatar = UserProfile.objects.get(user_id = request.user.id).avatar
	return render(request, 'app_classes/manualChecking.html', {'avatar':avatar, 'active_nav':'CLASSES', 'sections':sections})
>>>>>>> 3a24bf539ec1dc2d9c265f68db25d37a552a8c22
