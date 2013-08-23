from django.db import models
from app_auth.models import School, Student, Teacher

class Section(models.Model):
	school = models.ForeignKey(School)
	year_level = models.CharField(max_length=2)
	section_name = models.CharField(max_length=30)

	def __str__(self):
		return self.section_name

class Subject(models.Model):
	section = models.ForeignKey(Section)
	teacher = models.ForeignKey(Teacher)
	subject_name = models.CharField(max_length=30)
	academic_year = models.CharField(max_length=4)
	key = models.CharField(max_length=32, unique=True)

	def __str__(self):
		return self.subject_name

class ClassList(models.Model):
	subject = models.ForeignKey(Subject)
	student = models.ForeignKey(Student)
	status = models.IntegerField(max_length=1)

	def __str__(self):
		return u'%s, %s' % (self.subject.user_profile.user.last_name, self.subject.user_profile.user.first_name)


