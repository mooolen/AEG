from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	avatar = models.ImageField(upload_to='static/app_auth/images/avatars/')
	street = models.TextField()
	province = models.TextField()
	municipality = models.TextField()
	phone_number = models.TextField(max_length=7)
	

	def __str__(self):
		return u'%s, %s' % (self.user.last_name, self.user.first_name)

class School(models.Model):
	name = models.CharField(max_length=100)
	short_name = models.CharField(max_length=20)
	address = models.TextField()

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['name']

class Teacher(models.Model):
	user_profile = models.ForeignKey(UserProfile)
	school = models.ManyToManyField(School)
	
	def __str__(self):
		return u'%s, %s' % (self.user_profile.user.last_name, self.user_profile.user.first_name)

class Student(models.Model):
	user_profile = models.ForeignKey(UserProfile)
	school = models.ForeignKey(School)

	def __str__(self):
		return u'%s, %s' % (self.user_profile.user.last_name, self.user_profile.user.first_name)

class Note(models.Model):
    user = models.ForeignKey(User)
    pub_date = models.DateTimeField()
    title = models.CharField(max_length=200)
    body = models.TextField()

    def __str__(self):
        return self.title
