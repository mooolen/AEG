from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from app_auth.models import School, Student, Teacher
from django.forms.widgets import TextInput, Select

class Section(models.Model):
	school = models.ForeignKey(School, related_name='schools')
	year_level = models.CharField(max_length=2)
	section_name = models.CharField(max_length=30)

	def __str__(self):
		return u'%s - %s' % (self.year_level, self.section_name)

	def getStudentCount(self):
		favetag_count = ClassList.objects.filter(section_id=self.id).count()
		return favetag_count

	class Meta:
		ordering = ['school']

class Subject(models.Model):
	subject_name = models.CharField(max_length=30)
	academic_year = models.CharField(max_length=4)
	teacher = models.ForeignKey(Teacher)
	key = models.CharField(max_length=32, unique=True)

	def __str__(self):
		return self.subject_name

class SectionForm(ModelForm):
	class Meta:
		model = Section
		fields = ('school', 'year_level', 'section_name')
		#exclude = ('title',)
		widgets = {
          'school': Select(attrs={'class' : 'select-block span3'}),
          'year_level': Select(attrs={'class' : 'select-block span3'}),
          'section_name': Select(attrs={'class' : 'select-block span3'})
        }

class Classes(models.Model):
	school = models.ForeignKey(School)
	section = models.ForeignKey(Section)
	subject = models.ForeignKey(Subject)
	teacher = models.ForeignKey(Teacher)

	def __str__(self):
		return u'%s-%s-%s' % (self.school.short_name, self.subject.subject_name, self.teacher.user_profile.user.last_name)

	class Meta:
		ordering = ['school', 'section', 'subject']

class ClassesForm(ModelForm):
	class Meta:
		model = Classes
		exclude = ('teacher',)
		fields = ('school', 'section', 'subject')

	def __init__(self, *args, **kwargs):
		super(ClassesForm, self).__init__(*args, **kwargs)
		self.fields['school'].widget.attrs.update({'class': 'select-block span12'})
		self.fields['section'].widget.attrs.update({'class': 'select-block span12'})
		self.fields['subject'].widget.attrs.update({'class': 'select-block span12'})

class ClassList(models.Model):
	classes = models.ForeignKey(Classes)
	student = models.ManyToManyField(Student)
	status = models.IntegerField(max_length=1)
	section_id = models.ForeignKey(Section)

	def __str__(self):
		return u'%s, %s' % (self.classes.section, self.classes.subject)