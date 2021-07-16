from os import name
from django.urls import path
from . import views

urlpatterns = [
	path('branches/', views.branches, name='gitwrapper.api.branches'),
	path('branches/<str:branchname>/commits/', views.commits, name='gitwrapper.api.commits'),
	path('commits/<str:commitid>/', views.commit_detail, name="gitwrapper.api.commitdetail"),
	path('diff/<str:base>/<str:compare>/', views.compare, name="gitwrapper.api.compare"),
	path('merge/', views.PullRequestView().as_view(), name="gitwrapper.api.merge"),
	path('closepullrequest/<int:id>/', views.close_pull_request, name="gitwrapper.api.closepr"),
]
