from django.apps import AppConfig
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class StaffConfig(AppConfig):
    name = 'staff'

from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

content_type = ContentType.objects.get_for_model(Group)
permission = Permission.objects.create(codename='group_full',
                                       name='Gruppe ist voll',
                                       content_type=content_type)
