from django import forms
from app_classes.models import Section
from app_auth.models import School
from django.utils.html import strip_tags

class addClassForm(forms.Form):
	school = forms.ModelChoiceField(label='School', queryset=School.objects.all(), widget=forms.Select(attrs={'class':'select select-block span12', }))
	year_level = forms.CharField(label='Level', widget=forms.TextInput(attrs={'type':'text', 'class': 'span4', 'placeholder': 'Year Level', 'min': 1, }))
	section_name = forms.CharField(label='Section Name', widget=forms.TextInput(attrs={'type':'text', 'class': 'span4', 'placeholder': 'Class Name',}))

	class Meta:
		model = Section