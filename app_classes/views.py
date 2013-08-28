from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import addClassForm
from app_classes.models import SectionForm

@login_required(redirect_field_name='', login_url='/')
def dashboard(request):
	return render(request, 'app_classes/dashboard2.html')

@login_required(redirect_field_name='', login_url='/')
def class_teacher(request):
	return render(request, 'app_classes/class_teacher.html')

@login_required(redirect_field_name='', login_url='/')
def teacher_addNewClass(request):
	addClass_form = addClassForm()
	return render(request, 'app_classes/teacher_addNewClass.html', 
			{'addClassForm' : addClass_form, 'next_url': '/class_teacher'})

@login_required(redirect_field_name='', login_url='/')
def submit(request):
	if request.method == "POST":
		form_class = SectionForm(data=request.POST)
		success_url = request.POST.get("next_url", "/")
		if form_class.is_valid():
			form_class.save()
			return redirect(success_url)
		else:
			addClass_form = addClassForm()
			return render(request, 'app_classes/teacher_addNewClass.html',
				{'addClassForm' : addClassForm, 'next_url': '/class_teacher'})