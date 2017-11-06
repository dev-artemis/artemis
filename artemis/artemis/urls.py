"""artemis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, static, include
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponseRedirect

from base.views import Home, OmniSearchResponse
from lesson.views import index, all_events

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^$', Index, name='index'),
    # url(r'^home/', LessonCalendar, name='lesson_calendar_event'),
    url(r'^$', index, name='index'),
    url(r'^all_events/', all_events, name='all_events'),
    url(r'^student/', include('artemis.student.urls', namespace='student')),
    url(r'^lesson/', include('artemis.lesson.urls', namespace='lesson')),
    url(r'^teacher/', include('artemis.teacher.urls', namespace='teacher')),
    url(r'^omnisearchajax/$', OmniSearchResponse.as_view(), name="omnisearch")
]

urlpatterns += static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
