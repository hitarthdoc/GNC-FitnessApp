from django.db import models

from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.dispatch import receiver
from django_countries.fields import CountryField
from django.utils.translation import ugettext as _
from localflavor.in_.in_states import STATE_CHOICES
# Create your models here.


class Center(models.Model):
    """Center represents an Ymht Center
    """

    name = models.CharField(max_length=50, help_text=_("Center Name"))
    parent = models.ForeignKey('self', null=True, default=None, on_delete=models.CASCADE)
    is_displayed = models.BooleanField(default=True, help_text=_("Should the center be displayed?"))

    def __str__(self):
        return "Center: {}".format(self.name)


    def save(self, *args, **kwargs):
        """Filter fields before save

        Strip trailing whitespaces and comma characters from name field.
        convert to lowercase
        """

        self.name = self.name.rstrip(string.whitespace+',').title()
        super().save(*args, **kwargs)



class Address(models.Model):
    """Address represents an Event Address
    """

    # Validators
    ONLY_DIGITS_VALIDATOR = RegexValidator(regex=r'^[0-9]*$',
                                message=_("Only digits allowed."))

    address_1 = models.CharField(max_length=128, help_text=_("Address 1"))
    address_2 = models.CharField(max_length=255, blank=True,
                                help_text=_("Address 2"))
    city = models.CharField(max_length=60, help_text=_("City"))
    state = models.CharField(max_length=30, choices=STATE_CHOICES,
                            help_text=_("State"))
    country = CountryField(help_text=_("Country"))
    zip_code = models.CharField(max_length=6, validators=[ONLY_DIGITS_VALIDATOR,],
                                help_text=_("Zip Code"))
    raw = models.TextField(blank=True)

    def __str__(self):
        return "Address: {}".format(self.raw)

    def save(self, *args, **kwargs):
        """Filter fields before save

        Strip trailing whitespaces and comma characters from address fields.
        build raw field to represent complete address as a string
        """

        self.address_1 = self.address_1.rstrip(string.whitespace+',')
        self.address_2 = self.address_2.rstrip(string.whitespace+',')
        self.city = self.city.rstrip(string.whitespace+',').title()
        self.raw = '{},\n{},\n{}-{},\n{},\n{}\n'.format(
                self.address_1, self.address_2, self.city,
                self.state, self.country, self.zip_code)

        super().save(*args, **kwargs)



class Participant(models.Model):
    """Pariticpant represents an profile of event pariticipant
    center field is an foreign key to :model:`base.Center`
    """

    # Choices
    GENDER_FEMALE = 'female'
    GENDER_MALE = 'male'
    GENDER_CHOICES = (
            (GENDER_FEMALE, 'Female'),
            (GENDER_MALE, 'Male'))

    # Validators
    MOBILE_VALIDATOR = RegexValidator(regex=r'^\+?1?\d{9,15}$',
            message="Mobile Number must be entered in the format:\
                    '+999999999999'. Up to 15 digits allowed.")

    first_name = models.CharField(max_length=50, help_text=_("First Name"))
    last_name = models.CharField(max_length=50, help_text=_("Last Name"))
    date_of_birth = models.DateField(help_text=_("Date Of Birth"))
    mobile = models.CharField(max_length=15, validators=[MOBILE_VALIDATOR,],
                            help_text=_("Mobile Number. Add +91 prefix"))
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES,
                                default=GENDER_MALE)
    center = models.ForeignKey(Center, on_delete=models.CASCADE,
                                help_text=_("Center"))
    other_center = models.CharField(max_length=50, help_text=_(
                            "Center name if not available above"), blank=True)

    # Currently we are keeping this field optional
    email = models.EmailField(blank=True, help_text=_("Email"))


    def __str__(self):
        return "Participant: {} {}\n {} {}".format(
                self.first_name, self.last_name, self.center, self.mobile)

