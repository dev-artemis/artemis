from django.conf.urls import url, static, include
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponseRedirect

from views import StudentView

urlpatterns = [
    url(r'^(?P<pk>\d+)$', StudentView.as_view(), name='student')
]
