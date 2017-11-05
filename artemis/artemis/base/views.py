from django.http import HttpResponse, JsonResponse, Http404
from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from django.views import View
from django.apps import apps

import datetime
import json
from collections import Counter

from ..student.models import Student, Contact

class Home(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        html = "<html><body>It is now {}.</body></html>".format(datetime.datetime.now())
        return context


class OmniSearchResponse(View):

    def get(self, request, *args, **kwargs):
        if request.GET.get('term'):
            search_text = request.GET.get('term')
            search_text_split = search_text.split(" ")
            search_text_list = [x for x in search_text_split if x]

            json_result = []
            student_result_list = []
            contact_result_list = []

            for word in search_text_list:
                student_result_list.append((Student.objects.filter(first_name__icontains=word)|\
                Student.objects.filter(middle_name__icontains=word)|\
                Student.objects.filter(last_name__icontains=word))[:10])

                contact_result_list.append((Contact.objects.filter(first_name__icontains=word)|\
                Contact.objects.filter(middle_name__icontains=word)|\
                Contact.objects.filter(last_name__icontains=word))[:10])

            student_id_count = Counter(x for xs in student_result_list for x in set(xs))
            contact_id_count = Counter(x for xs in contact_result_list for x in set(xs))

            for student, count in student_id_count.items():
                if count == len(search_text_list):
                    student_json_dict = {}
                    student_json_dict["id"] = student.id
                    student_json_dict["model"] = "Student"
                    student_json_dict["value"] = "{}, {}".format(student, student.form)
                    json_result.append(student_json_dict)

            for contact, count in contact_id_count.items():
                if count == len(search_text_list):
                    contact_json_dict = {}
                    contact_json_dict["id"] = contact.id
                    contact_json_dict["model"] = "Contact"
                    contact_json_dict["value"] = str(contact)
                    json_result.append(contact_json_dict)

            return HttpResponse(json.dumps({"result":json_result}), content_type="application/json")
        elif request.GET.get("searchtext[]"):
            search = request.GET.get("searchtext[]")
            model_id, model = search.split("$")

            if model in ["Student", "Contact"]:
                model_obj = apps.get_model('student', model)
            obj = model_obj.objects.get(pk=model_id)

            return redirect(obj)
        else:
            raise Http404()
