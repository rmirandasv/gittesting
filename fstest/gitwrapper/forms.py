from django.forms import ModelForm
from . import models

class PullRequestForm(ModelForm):
	class Meta:
		model = models.PullRequest
		fields = ['title', 'description', 'base', 'compare', 'status']