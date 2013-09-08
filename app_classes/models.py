from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from app_auth.models import School, Student, Teacher
from django.forms.widgets import TextInput, Select
from datetime import datetime

class Class(models.Model):
	school = models.ForeignKey(School)
	year_level = models.CharField(max_length=2)
	section = models.CharField(max_length=30)
	subject = models.CharField(max_length=30)
	academic_year = models.CharField(max_length=20)
	teacher = models.ForeignKey(Teacher)
	student = models.ManyToManyField(Student)
	key = models.CharField(max_length=32, unique=True)
	date_created = models.DateTimeField(default=datetime.now)
	is_active = models.IntegerField(default=0)

	def __str__(self):
		return u'%s-%s %s' % (self.year_level, self.section, self.subject)

class ClassForm(ModelForm):
	class Meta:
		model = Class
		exclude = ('teacher', 'student', 'key', 'date_created', 'is_active')
		widgets = {
          'school': Select(attrs={'class' : 'select-block span3'}),
          'year_level': Select(attrs={'class' : 'select-block span3'}),
          'section': Select(attrs={'class' : 'select-block span3'}),
          'academic_year': Select(attrs={'class' : 'select-block span3'}),
        }