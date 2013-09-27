try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
   
from app_registration import signals
from django.shortcuts import render_to_response, render, redirect, get_object_or_404
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.template import RequestContext
from django.db.models import Q
from django.contrib.auth import (
	REDIRECT_FIELD_NAME, login, logout, authenticate
)
from  django.contrib.auth.views import logout_then_login
from django.contrib.auth.models import User, check_password
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.core.context_processors import csrf
from app_auth.models import UserProfile, passwordForm, UserProfile, Student, Teacher, School
from app_classes.models import Class
from app_essays.models import Essay, EssayResponse
from app_essays.models import GradingSystem, GradeSysForm, gradeForm, Grade
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .forms import LoginForm, PasswordForm, ProfileForm, schoolForStudent, schoolForTeacher, GradeForm

class LoginView(FormView):
	form_class = LoginForm
	redirect_field_name = REDIRECT_FIELD_NAME
	template_name = 'app_auth/login.html'
	success_url = '/dashboard'
	
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			return HttpResponseRedirect(self.get_success_url())
		else:
			return super(LoginView, self).dispatch(request, *args, **kwargs)
	
	def form_valid(self, form, request):
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
			
		user = authenticate(username=username, password=password)
			
		if user is not None:
			if user.is_active:
				login(self.request, user)
				return HttpResponseRedirect(self.get_success_url())			
		else:		
			return self.form_invalid(form, request)
	
	def form_invalid(self, form, request):
		return render_to_response( self.template_name , {
			'errors': 1,
			'form' : form, 
		},  RequestContext(request))
	
	def get_success_url(self):
		if self.success_url:
			redirect_to = self.success_url
		else:
			redirect_to = self.request.REQUEST.get(self.redirect_field_name, '')

		netloc = urlparse(redirect_to)[1]
		
		if not redirect_to:
			redirect_to = settings.LOGIN_REDIRECT_URL
		elif netloc and netloc != self.request.get_host():
			redirect_to = settings.LOGIN_REDIRECT_URL
		return redirect_to
	  
	def post(self, request, *args, **kwargs):
		c = {}
		c.update(csrf(request))
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		
		if form.is_valid():
			return self.form_valid(form, request)
		else:				
			return self.form_invalid(form, request)

def user_logout(request):
    return logout_then_login(request,login_url='/')

@login_required(redirect_field_name='', login_url='/')
def profile_edit(request, success=None):
	user_info = UserProfile.objects.filter(user_id = request.user.id)
	power = False

	if request.method == "POST":
		formProfile = ProfileForm(request.POST, request.FILES)
		schoolForm = schoolForStudent(request.POST)
		if request.user.is_staff:
			schoolForm = schoolForTeacher(request.POST)
		power = True

		if schoolForm.is_valid():
			if request.user.is_staff:
				temp = schoolForm.cleaned_data['school']
				teacher = Teacher.objects.filter(user=request.user)
				if not teacher.exists():
					teacher = Teacher.objects.create(user=request.user)
					teacher.save()
				else:
					teacher = teacher.get(user=request.user)
					teacher.school.clear()
				for school in temp:
					print(school)
					teacher.school.add(school)
			else:
				temp = schoolForm.cleaned_data
				student = Student.objects.filter(user=request.user)
				if not student.exists():
					student = Student.objects.create(user=request.user, school=temp['school'])
		if formProfile.is_valid():
			temp = formProfile.cleaned_data
			if user_info.exists():
				#userProfile update
				userProfile_info = user_info.get(user_id=request.user.id)
				userProfile_info.avatar = userProfile_info.avatar

				if not temp['avatar']:
					userProfile_info.avatar = 'images/avatars/user.png'
				else:
					userProfile_info.avatar = temp['avatar']	
				userProfile_info.street = temp['street']
				userProfile_info.municipality = temp['municipality']
				userProfile_info.province = temp['province']
				userProfile_info.phone_number = temp['phone_number']
				userProfile_info.save()

			else:	
				UserProfile.objects.create(avatar=temp['avatar'], user_id=request.user.id, street=temp['street'], municipality=temp['municipality'], province=temp['province'], phone_number=temp['phone_number'])
				
			#user update
			USER_info = User.objects.get(id=request.user.id)
			USER_info.last_name = temp['last_name']
			USER_info.first_name = temp['first_name']
			USER_info.email = temp['email']
			USER_info.username = temp['username']
			USER_info.save()
			return redirect("/dashboard")
	
	if user_info.exists():
		schoolForm = schoolForStudent()
		user_info = user_info.get(user_id=request.user.id)
		if request.user.is_staff:
			schoolForm = schoolForTeacher(initial={'school':Teacher.objects.get(user=request.user).school.values_list('id',flat=True)})
		
		avatar = user_info.avatar
		if not power:
			try:
				schoolForm = schoolForStudent(initial={'school':Student.objects.get(user=request.user).school})
			except:
				pass
			if request.user.is_staff:
				schoolForm = schoolForTeacher(initial={'school':Teacher.objects.get(user=request.user).school.values_list('id',flat=True)})
			formProfile = ProfileForm(initial={
				'last_name':request.user.last_name, 'first_name':request.user.first_name, 'email':request.user.email, 'avatar':user_info.avatar,
				'username': request.user.username, 'street':user_info.street, 'municipality':user_info.municipality,
				'province': user_info.province, 'phone_number': user_info.phone_number
			})
	else:
		schoolForm = schoolForStudent()
		if request.user.is_staff:
			schoolForm = schoolForTeacher()
		avatar = 'images/avatars/user.png'
		formProfile = ProfileForm(initial={'last_name':request.user.last_name, 'first_name':request.user.first_name, 'email':request.user.email,
			'username': request.user.username,})
	return render(request, 'app_auth/profile.html', {'avatar': avatar, 'success':success, 'formProfile':formProfile, 'schoolForm':schoolForm})

@login_required(redirect_field_name='', login_url='/')
def password_edit(request, success=None):
	user_info = UserProfile.objects.filter(user_id = request.user.id)
	if not user_info.exists():
		return redirect("/profile")
	user_info = user_info.get(user_id = request.user.id)
	avatar = user_info.avatar
	err = None
	power = False
	if request.user.is_staff:
		power = True
	if request.method == "POST":
		form_class = PasswordForm(data=request.POST)
		if form_class.is_valid():
			forms = form_class.cleaned_data
			password = forms['password']
			newPassword = forms['ConfPassword']
			oldPassword = forms['OldPassword']
			u = User.objects.get(id=request.user.id)

			if u.check_password(oldPassword) and password == newPassword:
				u.set_password(newPassword)
				u.save()
				success = 'You have changed your password.'
			else:
				err = 'Passwords did not matched.'
	else:
		form_class = PasswordForm()
	gradingSystem = GradingSystem.objects.filter(created_by=request.user)
	formSys = GradeSysForm()
	formGrade = gradeForm()
	return render(request, 'app_auth/changePassword.html', {'avatar': avatar, 'power':power,'user_info':user_info, 'formGrade':formGrade,'formSys':formSys,'form':form_class, 'error': err, 'success':success, 'gradingSystem':gradingSystem})

@login_required(redirect_field_name='', login_url='/')
def saveGrades(request):
	user_info = UserProfile.objects.filter(user_id = request.user.id)
	user_info = user_info.get(user_id = request.user.id)
	avatar = user_info.avatar
	success = None
	error = None
	if request.method == "POST":
		formSys = GradeSysForm(request.POST)
		formGrade = gradeForm(request.POST)
		if formGrade.is_valid() and formSys.is_valid():
			temp = formSys.save(commit=False)
			temp.created_by = request.user
			temp.save()
			success = 'New Grading System has been added.'
			#print(temp.id)
			names = []
			value = []
			names = request.POST.getlist('name')
			value = request.POST.getlist('value')
			print(value)
			for i in range(len(names)):
				print i, names[i]
				Grade.objects.create(grading_system=temp, name=names[i], value=value[i])
		else:
			error = 'Invalid input while adding new Grading System'
	form_class = PasswordForm()
	gradingSystem = GradingSystem.objects.filter(created_by=request.user)
	formSys = GradeSysForm()
	formGrade = gradeForm()
	power = True
	return render(request, 'app_auth/changePassword.html', {'avatar': avatar, 'error':error,'success':success,'power':power,'user_info':user_info,'form':form_class, 'formGrade':formGrade,'formSys':formSys,'gradingSystem':gradingSystem})

@login_required(redirect_field_name='', login_url='/')
def deleGradeSys(request, gradeSys_id):
	GradeSys = get_object_or_404(GradingSystem, pk=gradeSys_id)
	GradeSys.delete()
	return password_edit(request, 'You successfully deleted a Grading System.')


@login_required(redirect_field_name='', login_url='/')
def viewGradeSys(request, gradeSys_id, success=None):
	user_info = UserProfile.objects.filter(user_id = request.user.id)
	user_info = user_info.get(user_id = request.user.id)
	avatar = user_info.avatar
	success = None
	error = None
	#grade = get_object_or_404(Grade, pk=self.kwargs.get('grade_id'))
	GradeSys = get_object_or_404(GradingSystem, pk=gradeSys_id)
	grades = Grade.objects.filter(grading_system=GradeSys)
	#grades = get_list_or_404(Grade, relevantgs_pk= gradeSys_id)

	if request.method == "POST":
		grade_form = GradeForm(request.POST)

		if grade_form.is_valid():
			success = True
			name = grade_form.cleaned_data['name']
			value = grade_form.cleaned_data['value']
			success = "You have successfully added a grade on this grading system.";
			grade_form.save()
				
	else:
		grade_form=GradeForm()
	return render(request, 'app_auth/gradingSystemView.html', {'avatar': avatar, 'error':error,'success':success,'user_info':user_info, 'grade_form':grade_form, 'grades':grades})

@login_required(redirect_field_name='', login_url='/')
def deleGrade(request, grade_id):
	Grade_obj = get_object_or_404(Grade, pk=grade_id)
	Grade_obj.delete()
	return password_edit(request,'You have successfully deleted a Grade.')

def login_on_activation(sender, user, request, **kwargs):
    user.backend='django.contrib.auth.backends.ModelBackend' 
    login(request,user)
signals.user_activated.connect(login_on_activation)

def dashboard(request):
	User_Profile = UserProfile.objects.filter(user_id = request.user.id)
	if not User_Profile.exists():
		return redirect("/profile")
	avatar = User_Profile.get(user_id=request.user.id).avatar
	if len(Teacher.objects.filter(user_id = request.user.id)) > 0:
		class_count = Class.objects.filter(teacher=Teacher.objects.get(user=request.user), is_active=1).count()
		exam_count = Essay.objects.filter(instructor = Teacher.objects.get(user = request.user), status=1).filter(start_date__lte=timezone.now(), deadline__gte=timezone.now()).count()
		needs_grading_count =   EssayResponse.objects.filter(essay=Essay.objects.filter(instructor_id = Teacher.objects.get(user_id = request.user.id).id).filter(deadline__lt=timezone.now()), grade=None).count()
		return render(request, 'app_auth/teacher_dashboard.html', {'avatar': avatar, 'class_count':class_count, 'exam_count':exam_count, 'needs_grading_count':needs_grading_count})
	elif len(Student.objects.filter(user_id = request.user.id)) > 0:
		class_count = Class.objects.filter(student=Student.objects.get(user=request.user), is_active=1).count()
		exam_count = EssayResponse.objects.filter(~Q(essay__status=0), student=Student.objects.get(user_id = request.user.id)).filter(essay__start_date__lte=timezone.now(), essay__deadline__gte=timezone.now()).count()
		in_progress_count = EssayResponse.objects.filter(~Q(essay__status=1), student=Student.objects.get(user_id = request.user.id)).filter(essay__start_date__lte=timezone.now(), essay__deadline__gte=timezone.now()).count()
		return render(request, 'app_auth/student_dashboard.html', {'avatar': avatar, 'class_count':class_count, 'exam_count':exam_count, 'in_progress_count':in_progress_count})

@login_required(redirect_field_name='', login_url='/')
def help(request):
	User_Profile = UserProfile.objects.filter(user_id = request.user.id)
	if not User_Profile.exists():
		return redirect("/profile")
	avatar = User_Profile.get(user_id=request.user.id).avatar
	if len(Teacher.objects.filter(user_id = request.user.id)) > 0:
		return render(request, 'app_auth/teacher_help.html', {'avatar':avatar, 'active_nav':'DASHBOARD'})
	elif len(Student.objects.filter(user_id = request.user.id)) > 0:
		return render(request, 'app_auth/student_help.html', {'avatar':avatar, 'active_nav':'DASHBOARD'})

