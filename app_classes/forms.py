from django import forms

class MailForm(forms.Form):
	Email = forms.CharField(widget=forms.Textarea(attrs={'class':'span3'}))