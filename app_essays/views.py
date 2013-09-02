from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect

from app_auth.models import UserProfile, Teacher
from app_essays.models import Essay, GradingSystem, EssayForm
from app_classes.models import Subject

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
		form.fields['class_subject'].queryset = Subject.objects.filter(teacher_id = Teacher.objects.get(user_id = request.user.id).id)
	
	return render(request, 'app_essays/new_essay.html', {'avatar':avatar, 'errors':errors, 'form': form}, context_instance=RequestContext(request))

@login_required(redirect_field_name='', login_url='/')	
def list_essay(request):
	avatar = UserProfile.objects.get(user_id = request.user.id).avatar
	essays = Essay.objects.filter(instructor_id = Teacher.objects.get(user_id = request.user.id).id)
	
	return render(request, 'app_essays/list_essay.html', {'avatar':avatar, 'essays':essays})
	
	
	
