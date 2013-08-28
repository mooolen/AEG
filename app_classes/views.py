from django.shortcuts import render
from app_auth.models import UserProfile

def dashboard(request):
	avatar = UserProfile.objects.get(user_id = request.user.id).avatar
	return render(request, 'app_classes/dashboard.html', {'avatar':avatar})
	
def add_class(request):
	avatar = UserProfile.objects.get(user_id = request.user.id).avatar
	return render(request, 'app_classes/add_class.html', {'avatar':avatar})
	
def class_list(request):
	return 'hello'
