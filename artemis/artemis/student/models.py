from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.core.validators import RegexValidator



@python_2_unicode_compatible
class Year(models.Model):
    year = models.IntegerField()

    def __str__(self):
        return unicode(self.year)


@python_2_unicode_compatible
class Form(models.Model):
    form = models.CharField(max_length=250)
    year = models.ForeignKey(Year, related_name="form_year")

    def __str__(self):
        return "{} {}".format(self.year, self.form)

@python_2_unicode_compatible
class Address(models.Model):
    house_num = models.IntegerField()
    street_name = models.CharField(max_length=250)
    area = models.CharField(max_length=250)
    town_city = models.CharField(max_length=250)
    postcode = models.CharField(max_length=100)

    @property
    def primary(self):
        return self.is_primary

    @property
    def comma_separated(self):
        addr = ""
        spacer = ""
        house = self.house_num or self.street_name

        if self.house_num and self.street_name:
            house = "{} {}".format(self.house_num, self.street_name)

        for i in [house, self.area, self.town_city, self.postcode]:
            if i:
                addr += spacer + i
            if addr:
                spacer = ", "
        return addr

    @property
    def line_separated(self):
        addr = ""
        spacer = ""
        house = self.house_num or self.street_name

        if self.house_num and self.street_name:
            house = "{} {}".format(self.house_num, self.street_name)

        for i in [house, self.area, self.town_city, self.postcode]:
            if i:
                addr += spacer + i
            if addr:
                spacer = ",\n"
        return addr

    def __str__(self):
        return self.comma_separated

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'


@python_2_unicode_compatible
class Phone(models.Model):
    phone_type = models.CharField(choices=[["mob", "Mobile"], ["home", "Home"]], max_length=50)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,25}$', message="Phone number must be entered in the format: '+999999999'. Up to 25 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True)

    def __str__(self):
        return unicode(self.phone_number)


@python_2_unicode_compatible
class Student(models.Model):
    first_name = models.CharField(max_length=250)
    middle_name = models.CharField(max_length=250, blank=True)
    last_name = models.CharField(max_length=250)
    dob = models.DateField()
    form = models.ForeignKey(Form, related_name="student_form")
    photo = models.ImageField(upload_to="student", blank=True)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_absolute_url(self):
        return "/student/%i" % self.id


@python_2_unicode_compatible
class Contact(models.Model):
    first_name = models.CharField(max_length=250)
    middle_name = models.CharField(max_length=250, blank=True)
    last_name = models.CharField(max_length=250)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_absolute_url(self):
        return "/contact/%i" % self.id


class BaseLinkModel(models.Model):
    is_primary = models.BooleanField(default=True)

    @property
    def primary(self):
        return self.is_primary

    class Meta:
        abstract = True


@python_2_unicode_compatible
class StudentAddress(BaseLinkModel):
    student = models.ForeignKey(Student, related_name="student_address")
    address = models.ForeignKey(Address, related_name="address_student")

    def __str__(self):
        return '%s, %s' % (self.student, self.address)

    class Meta:
        verbose_name = 'Student Address'
        verbose_name_plural = 'Student Addresses'


@python_2_unicode_compatible
class StudentPhone(BaseLinkModel):
    student = models.ForeignKey(Student, related_name="student_phone")
    phone = models.ForeignKey(Phone, related_name="phone_student")

    def __str__(self):
        return '%s, %s' % (self.student, self.phone)


@python_2_unicode_compatible
class ContactAddress(BaseLinkModel):
    contact = models.ForeignKey(Contact, related_name="contact_address")
    address = models.ForeignKey(Address, related_name="address_contact")

    def __str__(self):
        return '%s, %s' % (self.contact, self.address)

    class Meta:
        verbose_name = 'Contact Address'
        verbose_name_plural = 'Contact Addresses'


@python_2_unicode_compatible
class ContactPhone(BaseLinkModel):
    contact = models.ForeignKey(Contact, related_name="contact_phone")
    phone = models.ForeignKey(Phone, related_name="phone_contact")

    def __str__(self):
        return '%s, %s' % (self.contact, self.phone)


@python_2_unicode_compatible
class StudentContactLink(models.Model):
    student = models.ForeignKey(Student, related_name="studentcontact_student")
    contact = models.ForeignKey(Contact, related_name="studentcontact_contact")

    def __str__(self):
        return '%s, %s' % (self.student, self.contact)

    class Meta:
        verbose_name = 'Student Contact'
        verbose_name_plural = 'Student Contacts'
