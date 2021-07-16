from django.shortcuts import render
from django.conf import settings


def home(request):
	dir = settings.GIT_DIR
	return render(request, 'gitwrapper/index.html', {
		'dir': dir,
	})