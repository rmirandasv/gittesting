from datetime import date
from django.utils.translation import gettext as _
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.conf import settings
from rest_framework.views import APIView
from . import serializers
from git import Repo
from gitwrapper import forms, models
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 


class CsrfCustomSessionAuthentication(SessionAuthentication):
	def enforce_csrf(self, request):
		return

repo = Repo(settings.GIT_DIR)

@api_view(['GET'])
def branches(request):
	repo_branches = repo.branches
	branchs = []
	for branch in repo_branches:
		branchs.append(serializers.Branch(name=branch))
	json = serializers.BranchSerializer(branchs, many = True).data
	data = {'data': json}
	return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET'])
def commits(request, branchname):
	repo_commits = repo.iter_commits(rev=branchname)
	commits = []
	for commit in repo_commits:
		commits.append(
			serializers.Commit(
				hexsha=commit.hexsha, 
				date=commit.committed_datetime, 
				message=commit.message,
				author=commit.author
				))
	json_commits = serializers.CommitSerializer(commits, many = True).data
	data = {'data': {
		'branch': branchname,
		'commits': json_commits
	}}
	return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET'])
def commit_detail(request, commitid):
	repo_commit = repo.commit(rev=commitid)
	commit = serializers.CommitDetail(
		hexsha=repo_commit.hexsha,
		author=repo_commit.author,
		author_email=repo_commit.author.email,
		commited_date=repo_commit.committed_datetime,
		message = repo_commit.message,
		file_list=repo_commit.stats.files
	)
	data = serializers.CommitDetailSerializer(commit).data
	data = {'data': data}
	return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET'])
def compare(request, base, compare):
	diffs = repo.git.diff(base, compare)
	data = {'diffs': diffs}
	return Response(data=data, status=status.HTTP_200_OK)

class PullRequestView(APIView):

	def get(self, request):
		requests = models.PullRequest.objects.all()
		data = serializers.PullRequestSerializer(requests, many=True).data
		return Response(data=data, status=status.HTTP_200_OK)

	def post(self, request):
		pr = forms.PullRequestForm(request.data)

		if pr.is_valid():
			if pr.cleaned_data['status'] == 3: # status 3 its merged, need to merge first
				try: 
					compare = repo.branches[pr.cleaned_data['compare']]
					base = repo.branches[pr.cleaned_data['base']]
					merge = repo.merge_base(compare, base)
					repo.index.merge_tree(base, merge)
					repo.index.commit(f"merge {base} into {compare}", parent_commits=(compare.commit, base.commit))
					pr.save()
					return Response(data={
						'message': _('Branches successfully merged')
					}, status=status.HTTP_200_OK)
				except:
					return Response(data={
						'message': _('Auto merge cannot be done due to conflicts. Please do a manual merge')
					}, status=status.HTTP_403_FORBIDDEN)
			pr.save()
			return Response(data={
				'message': _('Pull request successfully created')
			}, status=status.HTTP_201_CREATED)
		return Response(data={}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def close_pull_request(request, id):
	pr = models.PullRequest.objects.get(pk=id)
	pr.status = 2
	pr.save()
	data = serializers.PullRequestSerializer(pr).data
	return Response(data={'data': data}, status=status.HTTP_200_OK)