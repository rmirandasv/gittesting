from django.db import models
from django.utils.translation import gettext as _

class PullRequest(models.Model):
	STATUS = (
		(1, _('Open')),
		(2, _('Closed')),
		(3, _('Merged'))
	)
	title = models.CharField(max_length=50, blank=False, null=False)
	description = models.TextField(blank=False, null=False)
	base = models.CharField(max_length=255,blank=False, null=False)
	compare = models.CharField(max_length=255,blank=False, null=False)
	status = models.PositiveSmallIntegerField(choices=STATUS, default=1)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)