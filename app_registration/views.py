
import os
import hashlib
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from app_registration.forms import RegistrationForm
from django.shortcuts import render, get_object_or_404
from app_auth.models import UserProfile, Teacher, School
from django.db.models import Count
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def register(request):
	registration_form = RegistrationForm();
	return render(request, 'app_registration/register.html',
		{'RegistrationForm' : registration_form, 'next_url': '/'})
	