from django.forms import ModelForm
from restaurants import models

class RegistrationForm(ModelForm):

	class Meta:
		model = models.Restaurant
		exclude = ['owner']

