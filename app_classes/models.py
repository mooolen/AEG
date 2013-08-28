from django.db import models
from django.forms import ModelForm
from app_auth.models import School, Student, Teacher

class Section(models.Model):
	school = models.ForeignKey(School)
	year_level = models.CharField(max_length=2)
	section_name = models.CharField(max_length=30)
	emails = models.EmailField(max_length=30)

	def __str__(self):
		return self.section_name
	class Meta:
		ordering = ['school']

class Subject(models.Model):
	section = models.ForeignKey(Section)
	teacher = models.ForeignKey(Teacher)
	subject_name = models.CharField(max_length=30)
	academic_year = models.CharField(max_length=4)
	key = models.CharField(max_length=32, unique=True)

	def __str__(self):
		return self.subject_name

class SectionForm(ModelForm):
	class Meta:
		model = Section
		
	def __init__(self, *args, **kwargs):
		super(SectionForm, self).__init__(*args, **kwargs)
		self.fields['school'].widget.attrs.update({'class' : 'dropdown'})
		self.fields['year_level'].widget.attrs.update({'type':'number', 'class': 'span4', 'placeholder': 'Year Level', 'min': 1,})
		self.fields['section_name'].widget.attrs.update({'type':'text', 'class': 'span4', 'placeholder': 'Class Name',})
		self.fields['emails'].widget.attrs.update({'type':'textarea', 'class': 'input-xlarge span4', 'placeholder': 'Each emails are separeted by comma. Example: cheryleighverano@gmail.com, emsia@upd.edu.ph, molen.fenando@gmail.com', 'row': 8})


class ClassList(models.Model):
	subject = models.ForeignKey(Subject)
	student = models.ForeignKey(Student)
	status = models.IntegerField(max_length=1)

	def __str__(self):
		return u'%s, %s' % (self.subject.user_profile.user.last_name, self.subject.user_profile.user.first_name)


