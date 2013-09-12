from django.db import models
from django import forms
from django.forms import ModelForm, DateTimeInput, TextInput, Textarea
from django.utils import timezone
from django.utils.timezone import utc
from django.contrib.auth.models import User
from app_auth.models import Student, Teacher
from app_classes.models import Class
import datetime

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
	class_name = models.ForeignKey(Class)
	instructions = models.TextField()
	grading_system = models.ForeignKey(GradingSystem)	
	start_date = models.DateTimeField()
	deadline = models.DateTimeField()	
	duration_hours = models.IntegerField()
	duration_minutes = models.IntegerField()
	min_words = models.IntegerField()
	status = models.IntegerField()	#-1 - cancelled		0 - scheduled / not yet released	1 - on going	2 done/deadline
	date_created = models.DateTimeField(default=timezone.now())

	def __str__(self):
		return self.title
		
class EssayResponse(models.Model):
	essay = models.ForeignKey(Essay)
	student = models.ForeignKey(Student)
	response = models.TextField(blank=True, default="")
	time_started = models.DateTimeField(blank=True, null=True)
	status = models.IntegerField(default=0)	#0 - not yet started ; 1 - started / draft ; 2 - submitted
	grade = models.ForeignKey(Grade, null=True, blank=True)

	def __str__(self):
		return self.essay.title

	@property
	def time_remaining(self):
		essay_duration_sec = self.essay.duration_hours*60*60 + self.essay.duration_minutes*60
		if self.status != 0:
			delta = timezone.now() - self.time_started
			return essay_duration_sec - delta.seconds
		else:
			return essay_duration_sec

	@property
	def time_remaining_str(self):
		t = self.time_remaining
		hours = t/3600
		minutes = (t/60)%60
		time_str = str(hours) + ( ' hours' if hours > 1 else ' hour' ) if hours > 0 else ''
		time_str +=  str(minutes) + ( ' minutes' if minutes > 1 else ' minute' ) if minutes > 0 else ''
		return time_str

	@property
	def is_ongoing(self):
		if timezone.now() > self.essay.deadline():
			return False
		else:
			return True

class EssayForm(ModelForm):
	class Meta:
		model = Essay
		exclude = ('instructor', 'status', 'date_created')
		widgets = {
			'title': TextInput(attrs={'class':'input-xlarge span4', 'autofocus':'autofocus'}),
			'instructions': Textarea(attrs={'class':'input-xlarge span4', 'rows':'4'}),
			'min_words': TextInput(attrs={'class':'span1'}),
			#'grading_system': ModelChoiceField(queryset=GradingSystem.objects.all(), empty_label=None),
			'duration_hours': TextInput(attrs={'class':'span1'}),
			'duration_minutes': TextInput(attrs={'class':'span1'}),
			'start_date': DateTimeInput(attrs={'class':'span4', 'type':'date'}),
			'deadline': DateTimeInput(attrs={'class':'span4', 'type':'date'}),
		}
	
	def clean_duration_minutes(self):
		duration_minutes = self.cleaned_data['duration_minutes']

		if duration_minutes > 59:
			raise forms.ValidationError("Please enter a number from 0 to 59.")

		return duration_minutes

	def clean_start_date(self):
		startdate = self.cleaned_data['start_date']
		
		if datetime.datetime.date(startdate) < datetime.datetime.date(timezone.now()):
			raise forms.ValidationError("This date has already passed.")
		return startdate
	
	def clean_deadline(self):
		deadline = self.data['deadline']
		startdate = self.data['start_date']

		if deadline < startdate:
			raise forms.ValidationError("Date for deadline must be later than the start date.")
		return deadline

class EssayResponseForm(ModelForm):
	class Meta:
		model = EssayResponse
		fields = ['response']
		initial = {'response': 'aa' }
		widgets = {
			'response': Textarea(attrs={'class':'input-xlarge span4', 'rows':'10'}),
		}
