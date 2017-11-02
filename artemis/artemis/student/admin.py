from django.contrib import admin

from models import Year, Form, Student, Address, Phone, StudentAddress, StudentPhone, Contact, ContactAddress, ContactPhone, StudentContactLink

@admin.register(Year)
class YearAdmin(admin.ModelAdmin):
    model = Year
    fields = 'year',
    extra = 0

@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    model = Form
    fields = 'form', 'year',
    extra = 0

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    model = Student
    fields = 'first_name', 'middle_name', 'last_name', 'dob', 'form', 'photo', 
    extra = 0

@admin.register(Contact)
class StudentAdmin(admin.ModelAdmin):
    model = Contact
    fields = 'first_name', 'middle_name', 'last_name',
    extra = 0

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    model = Address
    fields = 'house_num', 'street_name', 'area', 'town_city', 'postcode',
    extra = 0

@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    model = Phone
    fields = 'phone_type', 'phone_number',
    extra = 0

@admin.register(StudentAddress)
class StudentAddressAdmin(admin.ModelAdmin):
    model = StudentAddress
    fields = 'student', 'address', 'is_primary',
    extra = 0

@admin.register(StudentPhone)
class StudentPhoneAdmin(admin.ModelAdmin):
    model = StudentPhone
    fields = 'student', 'phone', 'is_primary',
    extra = 0

@admin.register(ContactAddress)
class ContactAddressAdmin(admin.ModelAdmin):
    model = ContactAddress
    fields = 'contact', 'address', 'is_primary',
    extra = 0

@admin.register(ContactPhone)
class ContactPhoneAdmin(admin.ModelAdmin):
    model = ContactPhone
    fields = 'contact', 'phone', 'is_primary',
    extra = 0

@admin.register(StudentContactLink)
class ContactPhoneAdmin(admin.ModelAdmin):
    model = StudentContactLink
    fields = 'student', 'contact',
    extra = 0
