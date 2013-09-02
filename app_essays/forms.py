from django import forms
from app_essays.models import GradingSystem

class NewEssayForm(forms.Form):
	title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'input-xlarge span4', 'autofocus':'autofocus'}))
	instructions = forms.CharField(widget=forms.Textarea(attrs={'class':'input-xlarge span4', 'rows':'4'}))
	min_words = forms.CharField(widget=forms.TextInput(attrs={'class':'span1'}))
	grading_system = forms.ModelChoiceField(queryset=GradingSystem.objects.all(), empty_label=None)
	duration_hours = forms.CharField(widget=forms.TextInput(attrs={'class':'span1'}))
	duration_minutes = forms.CharField(widget=forms.TextInput(attrs={'class':'span1'}))
	deadline = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class':'span4', 'type':'date'}))
	
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
	
	#def __init__(self, *args, **kwargs):
	#	userid = kwargs.pop('accountid', None)
	#	super(NewEssayForm, self).__init__(*args, **kwargs)
	#	
	#	if accountid:
     #       self.fields['adminuser'].queryset = User.objects.filter(account=accountid)
