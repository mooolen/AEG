from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.db.models import Q

from app_auth.models import UserProfile, Student, Teacher
from app_essays.models import Essay, EssayResponse, GradingSystem, EssayForm, EssayResponseForm
from app_classes.models import Class

from datetime import datetime
import operator

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

			students = Class.objects.get(pk=Essay.objects.get(pk=data.pk).class_name.pk).student.all()

			for student in students:
				response = EssayResponse(essay=data, student=student)
				response.save()

			return HttpResponseRedirect('/essays/')
		else :
			errors = 1
		
	else:
		form = EssayForm()
		form.fields['class_name'].queryset = Class.objects.filter(teacher = Teacher.objects.get(user_id = request.user.id))
	
	return render(request, 'app_essays/teacher_newExam.html', {'avatar':avatar, 'active_nav':'EXAMS', 'errors':errors, 'form': form})

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
		return render(request, 'app_essays/teacher_viewExam.html',	{'avatar':avatar, 'active_nav':'EXAMS', 'no_essay':no_essay, 'essays':essays})

	#IF USER IS A STUDENT
	elif len(Student.objects.filter(user_id = request.user.id)) > 0:
		#essays = Essay.objects.filter(instructor_id = Teacher.objects.get(user_id = request.user.id).id)
		essay_responses = EssayResponse.objects.filter(~Q(status=2), student_id=Student.objects.get(user_id = request.user.id).id)
		return render(request, 'app_essays/student_viewEssay.html', {'avatar':avatar, 'active_nav':'EXAMS', 'essay_responses':essay_responses})
		
@login_required(redirect_field_name='', login_url='/')
def essay_details(request, essay_id):
	active_nav = "EXAMS"
	avatar = UserProfile.objects.get(user_id = request.user.id).avatar

	students = Class.objects.get(pk=Essay.objects.get(pk=essay_id).class_name.pk).student.all()
	essay = Essay.objects.get(pk=essay_id)
	essay_responses = sorted(EssayResponse.objects.filter(essay_id=essay.pk), key=operator.attrgetter('student.user.last_name', 'student.user.first_name')) # I used this way of sorting because we cannot use order_by() for case insensitive sorting :(
	return render(request, 'app_essays/teacher_viewExamInfo.html', {'avatar':avatar, 'active_nav':'EXAMS', 'essay':essay, 'essay_responses':essay_responses})
	
@login_required(redirect_field_name='', login_url='/')
def answer_essay(request, essay_response_id):
	active_nav = "EXAMS"
	avatar = UserProfile.objects.get(user_id = request.user.id).avatar
	essay_response = EssayResponse.objects.get(pk=int(essay_response_id))

	if essay_response.status == 0:
		essay_response.status = 1
		essay_response.time_started = datetime.now()
		essay_response.save()

	if request.method == 'POST':
		form = EssayResponseForm(request.POST, request)
		if form.is_valid():
			response_data = form.cleaned_data['response']
			essay_response.response = response_data
			essay_response.save()

			if 'draft' in request.POST:
				return HttpResponseRedirect('/essays')

			elif 'final' in request.POST:
				essay_response.status = 2
				essay_response.save()
				return HttpResponseRedirect('/essays/')
		else :
			errors = 1
		
	else:
		form = EssayResponseForm(initial={'response':essay_response.response})

	return render(request, 'app_essays/student_answerEssay.html', {'avatar':avatar, 'active_nav':'EXAMS', 'essay_response':essay_response, 'form':form})

@login_required(redirect_field_name='', login_url='/')
def essay_submission(request, essay_response_id):
	active_nav = "EXAMS"
	avatar = UserProfile.objects.get(user_id = request.user.id).avatar
	essay_response = EssayResponse.objects.get(pk=int(essay_response_id))

	return render(request, 'app_essays/teacher_viewEssaySubmission.html', {'avatar':avatar, 'active_nav':'EXAMS', 'essay_response':essay_response})