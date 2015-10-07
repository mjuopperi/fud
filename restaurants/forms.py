from django import forms
from restaurants import models

class RegistrationForm(forms.ModelForm):

	class Meta:
		model = models.Restaurant
		exclude = ['owner']

