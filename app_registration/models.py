from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	avatar = models.ImageField(upload_to='images/avatars/')
	street = models.TextField(blank=True)
	province = models.TextField(blank=True)
	municipality = models.TextField(blank=True)
	phone_number = models.TextField(max_length=7, blank=True)
	

	def __str__(self):
		return u'%s, %s' % (self.user.last_name, self.user.first_name)