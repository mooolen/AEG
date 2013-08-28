from django.shortcuts import render
<<<<<<< HEAD
from app_auth.models import UserProfile
=======
from django.contrib.auth.decorators import login_required
>>>>>>> f93d7213a3fe3570e6c2d4f2cb223a106252f3d9

from app_classes.forms import addClassForm

@login_required(redirect_field_name='', login_url='/')
def dashboard(request):
<<<<<<< HEAD
	avatar = UserProfile.objects.get(user_id = request.user.id).avatar
	return render(request, 'app_classes/dashboard.html', {'avatar':avatar})
	
def add_class(request):
	avatar = UserProfile.objects.get(user_id = request.user.id).avatar
	return render(request, 'app_classes/add_class.html', {'avatar':avatar})
	
def class_list(request):
	return 'hello'
=======
	return render(request, 'app_classes/dashboard2.html')

@login_required(redirect_field_name='', login_url='/')
def class_teacher(request):
	return render(request, 'app_classes/class_teacher.html')

@login_required(redirect_field_name='', login_url='/')
def teacher_addNewClass(request):
	addClass_form = addClassForm(data=request.POST)
	return render(request, 'app_classes/teacher_addNewClass.html', 
			{'addClassForm' : addClassForm, })
>>>>>>> f93d7213a3fe3570e6c2d4f2cb223a106252f3d9
