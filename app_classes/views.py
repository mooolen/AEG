
import os
import hashlib
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from app_classes.models import Class, ClassForm, EditForm
from django.shortcuts import render, get_object_or_404
from app_auth.models import UserProfile, Teacher, School, Student
from django.db.models import Count
from django.db.models import Count
from django import forms
from django.forms.widgets import Textarea
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required(redirect_field_name='', login_url='/')
def dashboard(request):
	try:
		avatar = UserProfile.objects.get(user_id = request.user.id).avatar
	except UserProfile.DoesNotExist:
		avatar = 'images/avatars/users.png'
	return render(request, 'app_classes/dashboard2.html', {'avatar':avatar, 'active_nav':'DASHBOARD'})
	
def add_class(request):
	avatar = UserProfile.objects.get(user_id = request.user.id).avatar
	return render(request, 'app_classes/add_class.html', {'avatar':avatar})
	
def class_list(request):
	avatar = UserProfile.objects.get(user_id = request.user.id).avatar
	return render(request, 'app_classes/dashboard2.html', {'avatar': avatar})

@login_required(redirect_field_name='', login_url='/')
def class_teacher(request, err=None, success=None):
	User_Profile = UserProfile.objects.get(user_id = request.user.id)
	teacher = Teacher.objects.filter(user=request.user)
	hasClasses = None
	link = 'app_classes/class_teacher.html'
	if teacher.exists():
		sections = Class.objects.filter(teacher=teacher)
	else:
		student = Student.objects.filter(user=request.user)
		if student.exists():
			link = 'app_classes/viewClasses.html'
			sections = Class.objects.filter(student=student)
		else:	
			hasClasses = 'You have no permission to add Classes.'
	if not sections.exists():
		hasClasses = 'You don\'t have Classes yet'
	avatar = User_Profile.avatar
	return render(request, link, {'avatar':avatar, 'active_nav':'CLASSES', 'sections':sections, 'error': err, 'success':success, 'hasClasses':hasClasses})

@login_required(redirect_field_name='', login_url='/')
def teacher_addNewClass(request, add_form=None):
	avatar = UserProfile.objects.get(user_id = request.user.id).avatar
	addClass_form = add_form or ClassForm()
	teacher = Teacher.objects.filter(user=request.user)
	name = Class.objects.filter(teacher=teacher)
	addClass_form.fields['Emails'] = forms.CharField(widget=Textarea)
	return render(request, 'app_classes/teacher_addNewClass.html', 
			{'addClassForm' : addClass_form, 'next_url': '/classes', 'avatar':avatar, 'active_nav':'CLASSES', 'name':name})

@login_required(redirect_field_name='', login_url='/')
def submit(request):
	if request.method == "POST":
		form_class = ClassForm(data=request.POST)
		success_url = request.POST.get("next_url", "/")
		if form_class.is_valid():
			forms = form_class.cleaned_data
			school_info = forms['school']
			subject_info = forms['subject']
			yearType_info = forms['year_level']
			section_info = forms['section']
			academicYear_info = forms['academic_year']
			emails = request.POST['Emails']
			print(emails)
			try:
				teacher = Teacher.objects.get(user=request.user)
			except Teacher.DoesNotExist:
				return class_teacher(request, 'You don\'t have permission to add Classes.')

			class_info = Class.objects.filter(school=school_info).filter(section=section_info).filter(subject=subject_info).filter(teacher=teacher).filter(year_level=yearType_info).filter(academic_year=academicYear_info)
			if class_info.exists():
				return class_teacher(request, 'That Class already exists.')

			form = form_class.save(commit=False)
			form.teacher = teacher
			form.date_created = timezone.now()
			form.is_active = True

			random_data = os.urandom(128)
			random_data = hashlib.md5(random_data).hexdigest()[:16]

			form.key = random_data
			form.save()
			return redirect(success_url)
		else:
			return teacher_addNewClass(request, form_class)


@login_required(redirect_field_name='', login_url='/')
def edit(request, class_id):
	class_info = Class.objects.get(pk=class_id)
	formEdit = EditForm(initial={'school':class_info.school, 'year_level':class_info.year_level, 'section':class_info.section, 'academic_year':class_info.academic_year, 'subject':class_info.subject})
	avatar = UserProfile.objects.get(user_id = request.user.id).avatar
	return render(request, 'app_classes/teacher_editClass.html', {'avatar':avatar, 'active_nav':'CLASSES', 'class_info':class_info, 'formEdit':formEdit})
			
@login_required(redirect_field_name='', login_url='/')
def manualChecking(request):
	#sections = Section.objects.annotate(number_of_entries=Count('section_name')).select_related('school__short_name','section_name')
	#avatar = UserProfile.objects.get(user_id = request.user.id).avatar
	#return render(request, 'app_classes/manualChecking.html', {'avatar':avatar, 'active_nav':'CLASSES', 'sections':sections})
	return render(request, 'app_classes/manualChecking.html')

@login_required(redirect_field_name='', login_url='/')
def delete(request, class_id):
	class_info = get_object_or_404(Class, pk=class_id)
	class_info.delete()
	success_url = '/classes/'
	return class_teacher(request, 0, 'You successfully deleted a class.')

@login_required(redirect_field_name='', login_url='/')
def viewClassList(request, class_id):
	class_info = Class.objects.get(pk=class_id)
	avatar = UserProfile.objects.get(user_id = request.user.id).avatar
	return render(request, 'app_classes/viewClassList.html', {'studentList':class_info, 'active_nav':'CLASSES', 'avatar':avatar})