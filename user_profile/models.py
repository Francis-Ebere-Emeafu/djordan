from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


USERTYPE_CHOICES = (
    ('admin', 'Administrator'),
    ('frontdesk', 'Front Desk Officer'),
    ('laundry', 'Laundry Attendant'),
    ('store', 'Store Keeper'),
    ('bar', 'Bar Officer'),
    ('restaurant', 'Restaurant Personnel'),
    ('kitchen', 'Kitchen Officer'),
)


class UserProfile(models.Model):
    SELECT = 0
    MR = 1
    MRS = 2
    TITLE = enumerate(('Select', 'Mr', 'Mrs'))

    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    title = models.PositiveIntegerField(choices=TITLE, default=SELECT)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    usertype = models.CharField(max_length=20, choices=USERTYPE_CHOICES, default='front_desk', verbose_name='User Type')

    def __unicode__(self):
        return '{} {} {}'.format(self.title, self.first_name, self.last_name)
