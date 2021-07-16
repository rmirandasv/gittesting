from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns = [
	path('', views.home, name='gitwrapper.home'),
	path('api/', include('gitwrapper.api.urls')),
]
