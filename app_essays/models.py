from django.db import models
from django import forms
from django.forms import ModelForm, DateTimeInput, TextInput, Textarea

from django.contrib.auth.models import User
from app_auth.models import Student, Teacher
from app_classes.models import Subject, Classes

class GradingSystem(models.Model):
	name = models.CharField(max_length=50)
	created_by = models.ForeignKey(User)
	description = models.TextField(max_length=100)
	
	def __str__(self):
		return u'%s %s' % (self.name, self.description)

class Grade(models.Model):
	grading_system = models.ForeignKey(GradingSystem)
	name = models.CharField(max_length=20)
	value = models.FloatField()	

	def __str__(self):
		return self.name
		
class Essay(models.Model):
	title = models.CharField(max_length=100)
	instructor = models.ForeignKey(Teacher)
	class_subject = models.ForeignKey(Subject)
	instructions = models.TextField()
	grading_system = models.ForeignKey(GradingSystem)
	deadline = models.DateTimeField()	
	duration_hours = models.IntegerField()
	duration_minutes = models.IntegerField()
	min_words = models.IntegerField()
	status = models.IntegerField()

	def __str__(self):
		return self.title
		
class EssayResponse(models.Model):
	essay = models.ForeignKey(Essay)
	student = models.ForeignKey(Student)
	response = models.TextField()
	time_started = models.DateTimeField()
	status = models.IntegerField()
	grade = models.ForeignKey(Grade)

	def __str__(self):
		return self.essay.title
		
class EssayForm(ModelForm):
	class Meta:
		model = Essay
		exclude = ('instructor', 'status')
		widgets = {
			'title': TextInput(attrs={'class':'input-xlarge span4', 'autofocus':'autofocus'}),
			'instructions': Textarea(attrs={'class':'input-xlarge span4', 'rows':'4'}),
			'min_words': TextInput(attrs={'class':'span1'}),
			#'grading_system': ModelChoiceField(queryset=GradingSystem.objects.all(), empty_label=None),
			'duration_hours': TextInput(attrs={'class':'span1'}),
			'duration_minutes': TextInput(attrs={'class':'span1'}),
			'deadline': DateTimeInput(attrs={'class':'span4', 'type':'date'}),
		}
		
		def clean_duration_hours(self):
			duration_hours = self.cleaned_data['duration_hours']
		
			if not duration_hours.isdigit():
				raise forms.ValidationError("Please enter a number.")
			return duration_hours
		
		def clean_duration_minutes(self):
			duration_minutes = self.cleaned_data['duration_minutes']
		
			if not duration_minutes.isdigit():
				raise forms.ValidationError("Please enter a number.")
			return duration_minutes
	
		
class EssayReponse(ModelForm):
	class Meta:
		model = EssayResponse
		

