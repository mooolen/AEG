from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect

from app_auth.models import UserProfile, Student
from app_essays.models import Essay, GradingSystem, EssayForm
from app_classes.models import Class

@login_required(redirect_field_name='', login_url='/')
def new_essay(request):
	avatar = UserProfile.objects.get(user_id = request.user.id).avatar
	errors = 0;
	if request.method == 'POST':
		form = EssayForm(request.POST, request)
		if form.is_valid():
			cd = form.cleaned_data
			data = form.save(commit=False)
			data.instructor = Teacher.objects.get(user_id = request.user.id)
			data.status = 1
			data.save()
			return HttpResponseRedirect('/dashboard')
		else :
			errors = 1
		
	else:
		form = EssayForm()
		form.fields['class_name'].queryset = Class.objects.filter(teacher = Teacher.objects.get(user_id = request.user.id))
	
	return render(request, 'app_essays/teacher_newEssay.html', {'avatar':avatar, 'active_nav':'EXAMS', 'errors':errors, 'form': form})

@login_required(redirect_field_name='', login_url='/')	
def list_essay(request):
	active_nav = "EXAMS"
	avatar = UserProfile.objects.get(user_id = request.user.id).avatar
	no_essay = 0
	#IF USER IS A TEACHER
	if len(Teacher.objects.filter(user_id = request.user.id)) > 0:
		essays = Essay.objects.filter(instructor_id = Teacher.objects.get(user_id = request.user.id).id)
		if (len(essays) == 0 ):
			no_essay = 1	
		return render(request, 'app_essays/teacher_viewEssay.html',	{'avatar':avatar, 'active_nav':'EXAMS', 'no_essay':no_essay, 'essays':essays})

	#IF USER IS A STUDENT
	elif len(Student.objects.filter(user_id = request.user.id)) > 0:
		#essays = Essay.objects.filter(instructor_id = Teacher.objects.get(user_id = request.user.id).id)
		essays = Essay.objects.all()
		return render(request, 'app_essays/student_viewEssay.html', {'avatar':avatar, 'active_nav':'EXAMS', 'essays':essays})
		
@login_required(redirect_field_name='', login_url='/')
def essay_details(request, essay_id):
	active_nav = "EXAMS"
	avatar = UserProfile.objects.get(user_id = request.user.id).avatar
	essay = Essay.objects.get(pk=1) 
	return render(request, 'app_essays/teacher_viewEssayDetail.html', {'avatar':avatar, 'active_nav':'EXAMS', 'essay':essay})
	
	
