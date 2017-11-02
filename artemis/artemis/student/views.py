from django.views.generic import DetailView

from models import Student, StudentAddress, StudentPhone, StudentContactLink,\
ContactAddress, ContactPhone

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
        return context
