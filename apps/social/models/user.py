import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.utils.translation import gettext_lazy as _
from apps.social.common.validators import mobile_char_check


class BaseModel(models.Model):  # Base model for the application. Uses UUID for pk
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    class Meta:
        abstract = True


class User(BaseModel, AbstractUser):
    user_slug = AutoSlugField(populate_from=['username'], unique=True)  # install django_extensions
    is_online = models.BooleanField('Online', default=False)
    phone_number = models.CharField(
        'Phone number', blank=True, null=True,
        validators=[mobile_char_check], max_length=20,
        error_messages={'wrong_phone_number': _('Wrong phone number')},
        help_text='write your phone number like 9121133445')
    otp = models.IntegerField(null=True)

    REQUIRED_FIELDS = ['email','phone_number']
    def __str__(self):
        return super(User, self).get_full_name()

    class Meta:
        ordering = ['-last_login', 'is_online']
