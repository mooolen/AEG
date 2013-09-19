from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from app_auth.models import UserProfile
from django.db.models import Count
from django.contrib.auth.decorators import login_required

@login_required(redirect_field_name='', login_url='/')
def home(request):
	avatar = UserProfile.objects.get(user_id = request.user.id).avatar
	return render(request, 'app_student/home.html', {'avatar':avatar, 'active_nav':'DASHBOARD'})
	
@login_required(redirect_field_name='', login_url='/')
def answerExam(request):
	avatar = UserProfile.objects.get(user_id = request.user.id).avatar
	return render(request, 'app_student/answerExam.html', {'avatar':avatar, 'active_nav':'ESSAYS' })
	
@login_required(redirect_field_name='', login_url='/')
def viewClasses(request):
	avatar = UserProfile.objects.get(user_id = request.user.id).avatar
	return render(request, 'app_student/viewClasses.html', {'avatar':avatar, 'active_nav':'CLASSES'})
		
@login_required(redirect_field_name='', login_url='/')
def editProfile(request):
	avatar = UserProfile.objects.get(user_id = request.user.id).avatar
	return render(request, 'app_student/editProfile.html', {'avatar':avatar})
	
@login_required(redirect_field_name='', login_url='/')
def viewProfile(request):
	avatar = UserProfile.objects.get(user_id = request.user.id).avatar
	return render(request, 'app_student/viewProfile.html', {'avatar':avatar})
	
@login_required(redirect_field_name='', login_url='/')
def viewEssays(request):
	avatar = UserProfile.objects.get(user_id = request.user.id).avatar
	return render(request, 'app_student/viewEssays.html', {'avatar':avatar, 'active_nav':'ESSAYS'})
	
@login_required(redirect_field_name='', login_url='/')
def viewEssay(request):
	avatar = UserProfile.objects.get(user_id = request.user.id).avatar
	return render(request, 'app_student/viewEssay.html', {'avatar':avatar, 'active_nav':'ESSAYS'})
	
@login_required(redirect_field_name='', login_url='/')
def changePassword(request):
	avatar = UserProfile.objects.get(user_id = request.user.id).avatar
	return render(request, 'app_student/changePassword.html', {'avatar':avatar, 'active_nav':'ESSAYS'})
	