from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from app_classes.forms import addClassForm

@login_required(redirect_field_name='', login_url='/')
def dashboard(request):
	return render(request, 'app_classes/dashboard2.html')

@login_required(redirect_field_name='', login_url='/')
def class_teacher(request):
	return render(request, 'app_classes/class_teacher.html')

@login_required(redirect_field_name='', login_url='/')
def teacher_addNewClass(request):
	addClass_form = addClassForm(data=request.POST)
	return render(request, 'app_classes/teacher_addNewClass.html', 
			{'addClassForm' : addClassForm, })