from django import forms
from app_classes.models import Section
from app_auth.models import School
from django.utils.html import strip_tags

class addClassForm(forms.Form):
	school = forms.ModelChoiceField(label='School', queryset=School.objects.all(), widget=forms.Select(attrs={'class':'select select-block', }))
	year_level = forms.CharField(label='Level', widget=forms.TextInput(attrs={'type':'text', 'class': 'span4', 'placeholder': 'Year Level', 'min': 1, }))
	section_name = forms.CharField(label='Section Name', widget=forms.TextInput(attrs={'type':'text', 'class': 'span4', 'placeholder': 'Class Name',}))
	emails = forms.CharField(label='Emails', widget=forms.Textarea(attrs={'type':'text', 'class': 'input-xlarge span4', 'placeholder': 'Each emails are separeted by comma. Example: cheryleighverano@gmail.com, emsia@upd.edu.ph, molen.fenando@gmail.com',}))

	class Meta:
		model = Section
