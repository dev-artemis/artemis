from django.views.generic import DetailView

from models import Student, StudentAddress, StudentPhone, StudentContactLink,\
ContactAddress, ContactPhone
from artemis.teacher.models import ClassStudent
from artemis.lesson.models import LessonCalendarEvent
from fullcalendar.util import calendar_options, convert_field_names, date_handler

class StudentView(DetailView):
    model = Student
    template_name = "student/student.html"

    def get_context_data(self, **kwargs):
        context = super(StudentView, self).get_context_data(**kwargs)

        student = context["student"]

        #get student's address
        stud_addr = ""
        student_address = StudentAddress.objects.filter(student=student)
        for address_link in student_address:
            if address_link.is_primary:
                stud_addr = address_link.address.line_separated
                break
            else:
                stud_addr = address_link.address.line_separated
        context["student_addr"] = stud_addr

        #get student's phone
        stud_phone = ""
        student_phone = StudentPhone.objects.filter(student=student)
        for phone_link in student_phone:
            if phone_link.is_primary:
                stud_phone = phone_link.phone
                break
            else:
                stud_phone = phone_link.phone
        context["student_phone"] = stud_phone

        #get the contacts for the student
        contact_list = []
        student_contacts = StudentContactLink.objects.filter(student=student)
        for contact in student_contacts:
            contact_dict = {}
            contact_dict["contact_name"] = contact.contact

            contact_addr = ContactAddress.objects.filter(contact=contact.contact)
            for addr in contact_addr:
                if addr.is_primary:
                    contact_dict["contact_addr"] = addr.address.line_separated
                    break
                else:
                    contact_dict["contact_addr"] = addr.address.line_separated

            contact_phone = ContactPhone.objects.filter(contact=contact.contact)
            for phone_link in contact_phone:
                if phone_link.is_primary:
                    contact_dict["contact_phone"] = phone_link.phone
                    break
                else:
                    contact_dict["contact_phone"] = phone_link.phone

            contact_list.append(contact_dict)
        context["student_contacts"] = contact_list

        #get all classes the student is in, and from there determine where/when the classes are
        student_classes = ClassStudent.objects.filter(student=student)
        class_list = []
        for student_class in student_classes:
            class_list.append(student_class.clss)

        student_events = LessonCalendarEvent.objects.filter(lesson__clss_info__clss__in=class_list)
        for event in student_events:
            event.url = event.get_absolute_url()
            event.start = date_handler(event.start)
            event.end = date_handler(event.end)
            event.title = "{}. Room: {}".format(event.title, event.lesson.room)

        context["student_events"] = student_events
        return context
