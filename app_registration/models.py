from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from app_auth.models import School

class CustomRegistrationProfile(models.Model):
	user = models.ForeignKey(User, unique=True)
	first_name = models.CharField(max_length=200, blank=True)
	last_name = models.CharField(max_length=200, blank=True)
	school = models.ForeignKey(School)
