from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from django.utils.translation import gettext as _
from gitwrapper import models

class Branch:
	def __init__(self, name):
		self.name = name

class Commit:
	def __init__(self, hexsha, date, message, author):
		self.hexsha = hexsha
		self.date = date
		self.message = message
		self.author = author

class BranchSerializer(serializers.Serializer):
	name = serializers.CharField()

class CommitSerializer(serializers.Serializer):
	hexsha = serializers.CharField()
	date = serializers.DateTimeField(format="%d/%m/%y %H:%M:%S")
	message = serializers.CharField()
	author = serializers.CharField()

class CommitDetail:
	def __init__(self, hexsha, author, author_email, commited_date, message, file_list):
		self.hexsha = hexsha
		self.author = author
		self.author_email = author_email
		self.commited_date = commited_date
		self.message = message
		self.file_list = file_list

class CommitDetailSerializer(serializers.Serializer):
	hexsha = serializers.CharField()
	author = serializers.CharField()
	author_email = serializers.CharField()
	commited_date = serializers.DateTimeField(format="%d/%m/%y %H:%M:%S")
	message = serializers.CharField()
	file_list = serializers.ListField()

class Diff:
	def __init__(self, diffs):
		self.diffs = diffs

class DiffSerializer(serializers.Serializer):
	diffs = serializers.ListField()

class PullRequestSerializer(serializers.ModelSerializer):
	STATUS = (
		(1, _('Open')),
		(2, _('Closed')),
		(3, _('Merged'))
	)
	status = serializers.ChoiceField(STATUS)
	class Meta:
		model = models.PullRequest
		fields = ['id','title', 'description', 'base', 'compare', 'status', 'created_at', 'updated_at']