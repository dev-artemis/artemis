from django.http import HttpResponse
from django.views.generic.base import TemplateView

import datetime

class Home(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        html = "<html><body>It is now {}.</body></html>".format(datetime.datetime.now())
        return context
