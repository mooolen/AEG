from django import forms
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

class addClassForm(forms.Form):
	level = forms.CharField( label='Level', widget=forms.TextInput(attrs={'type':'text', 'class': 'span4', 'placeholder': 'Year Level',}))
	className = forms.CharField( label='Class Name', widget=forms.TextInput(attrs={'type':'text', 'class': 'span4', 'placeholder': 'Class Name',}))
	emails = forms.CharField( label='Emails', widget=forms.Textarea(attrs={'type':'text', 'class': 'input-xlarge span4', 'placeholder': mark_safe('Each emails are separeted by comma. \n Example: '),}))

	def is_valid(self):
		form = super(addClassForm, self).is_valid()
		for f, error in self.errors.iteritems():
			if f != '__all_':
				self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
		return form

	class Meta:
		fields = ['level', 'className', 'emails']
		model = User