from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(redirect_field_name='', login_url='/')
def dashboard(request):
	return render(request, 'app_student/student_home.html')

@login_required(redirect_field_name='', login_url='/')
def student_answerExam(request):
	return render(request, 'app_student/student_answerExam.html')
