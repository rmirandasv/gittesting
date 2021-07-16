from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
import json


class BranchesTestCase(APITestCase):
	def test_get_branches(self):
		url = reverse('gitwrapper.api.branches')
		response = self.client.get(url, format='json')
		data = json.loads(response.content)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertGreater(len(data['data']), 0)
		self.assertContains(response, 'master')

class CommitByBranchTestCase(APITestCase):
	def test_get_commits_by_branch(self):
		url = reverse('gitwrapper.api.commits', kwargs={'branchname': 'master'})
		response = self.client.get(url, format='json')
		jsondata = json.loads(response.content)
		self.assertEqual(jsondata['data']['branch'], 'master')

class CommitDetailTestCase(APITestCase):
	def setUp(self):
		url = reverse('gitwrapper.api.commits',kwargs={'branchname': 'master'})
		response = self.client.get(url, format='json')
		jsondata = json.loads(response.content)
		self.commitid = jsondata['data']['commits'][0]['hexsha']
		return super().setUp()

	def test_get_commit_details(self):
		url = reverse('gitwrapper.api.commitdetail', kwargs={'commitid': self.commitid})
		response = self.client.get(url, format='json')
		jsondata = json.loads(response.content)
		self.assertEqual(jsondata['data']['hexsha'], self.commitid)

class DiffTestCase(APITestCase):
	def test_get_diffs_between_branches(self):
		url = reverse('gitwrapper.api.compare', kwargs={'base': 'master', 'compare': 'develop'})
		response = self.client.get(url, forma='json')
		jsondata = json.loads(response.content)
		self.assertGreater(len(jsondata), 0)

class MergeTestCase(APITestCase):
	def test_create_pull_request(self):
		url = reverse('gitwrapper.api.merge')
		response = self.client.post(url, {
			'title': 'Testing pull requests',
			'description': 'Just testing pull request',
			'base': 'master',
			'compare': 'develop',
			'status': 1
		}, format='json')
		self.assertEquals(response.status_code, status.HTTP_201_CREATED)

class ClosePullRequest(APITestCase):
	def setUp(self):
		url = reverse('gitwrapper.api.merge')
		self.client.post(url, {
			'title': 'Testing pull request',
			'description': 'Just testing pull request',
			'base': 'master',
			'compare':'develop',
			'status': 1
		}, format='json')
		return super().setUp()

	def test_close_pull_request(self):
		url = reverse('gitwrapper.api.closepr', args=[1])
		response = self.client.post(url, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)