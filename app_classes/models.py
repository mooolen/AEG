from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from app_auth.models import School, Student, Teacher

class Section(models.Model):
	school = models.ForeignKey(School, related_name='schools')
	year_level = models.CharField(max_length=2)
	section_name = models.CharField(max_length=30)

	def __str__(self):
		return self.section_name

	def getStudentCount(self):
		favetag_count = ClassList.objects.filter(section_id=self.id).count()
		return favetag_count

	class Meta:
		ordering = ['school']

class Subject(models.Model):
	section = models.ForeignKey(Section)
	teacher = models.ForeignKey(Teacher)
	subject_name = models.CharField(max_length=30)
	academic_year = models.CharField(max_length=4)
	key = models.CharField(max_length=32, unique=True)

	def __str__(self):
		return u'%s-%s %s' % (self.section.year_level, self.section.section_name, self.subject_name)

class SectionForm(ModelForm):
	class Meta:
		model = Section
		
	def __init__(self, *args, **kwargs):
		super(SectionForm, self).__init__(*args, **kwargs)
		self.fields['school'].widget.attrs.update({'class' : 'dropdown'})
		self.fields['year_level'].widget.attrs.update({'type':'number', 'class': 'span4', 'placeholder': 'Year Level', 'min': 1,})
		self.fields['section_name'].widget.attrs.update({'type':'text', 'class': 'span4', 'placeholder': 'Class Name',})

class ClassList(models.Model):
	subject = models.ForeignKey(Subject)
	student = models.ForeignKey(Student)
	status = models.IntegerField(max_length=1)
	section_id = models.ForeignKey(Section)

	def __str__(self):
		return u'%s, %s' % (self.student.user_profile.user.last_name, self.student.user_profile.user.first_name)	
