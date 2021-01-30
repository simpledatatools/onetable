from django.db import models
from django.conf import settings
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone
from django.db.models import JSONField
from tinymce.models import HTMLField
import os

class Organization(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    last_updated = models.DateTimeField(auto_now_add=True)

    ORGANIZATION_STATUS = (
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('deleted', 'Deleted'),
    )

    status = models.CharField(
        max_length=25,
        choices=ORGANIZATION_STATUS,
        blank=False,
        default='active',
    )

    # TODO add @property for organization users

    def __str__(self):
        return self.name


class OrganizationUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    ORGANIZATION_USER_STATUS = (
        ('active', 'Active'),
        ('deleted', 'Deleted'),
    )

    status = models.CharField(
        max_length=25,
        choices=ORGANIZATION_USER_STATUS,
        blank=False,
        default='active',
    )

    ORGANIZATION_USER_ROLE = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )

    role = models.CharField(
        max_length=25,
        choices=ORGANIZATION_USER_ROLE,
        blank=False,
        default='active',
    )


class App(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    last_updated = models.DateTimeField(auto_now_add=True)

    APP_STATUS = (
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('deleted', 'Deleted'),
    )

    status = models.CharField(
        max_length=25,
        choices=APP_STATUS,
        blank=False,
        default='active',
    )

    # TODO add @property for app users

    def __str__(self):
        return self.name


class AppUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    app = models.ForeignKey('App', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    PROJECT_USER_STATUS = (
        ('active', 'Active'),
        ('deleted', 'Deleted'),
    )

    status = models.CharField(
        max_length=25,
        choices=PROJECT_USER_STATUS,
        blank=False,
        default='active',
    )

    APP_USER_ROLE = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )

    role = models.CharField(
        max_length=25,
        choices=APP_USER_ROLE,
        blank=False,
        default='active',
    )


class Menu(models.Model):
    name = models.CharField(max_length=200)
    app = models.ForeignKey('App', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    last_updated = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField()

    MENU_STATUS = (
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('deleted', 'Deleted'),
    )

    status = models.CharField(
        max_length=25,
        choices=MENU_STATUS,
        blank=False,
        default='active',
    )

    def __str__(self):
        return self.name


class List(models.Model):
    name = models.CharField(max_length=200)
    app = models.ForeignKey('App', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    last_updated = models.DateTimeField(auto_now_add=True)

    LIST_STATUS = (
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('deleted', 'Deleted'),
    )

    status = models.CharField(
        max_length=25,
        choices=LIST_STATUS,
        blank=False,
        default='active',
    )

    @property
    def list_fields(self):
        # return ListField.objects.filter(list=self, status='active').order_by('order') \
        #     .select_related('list__app', 'list__created_user') \
        #     .select_related('created_user')
        return ListField.objects.filter(list=self, status='active').order_by('-order') \
            .select_related('list__app', 'list__created_user') \
            .select_related('created_user')

    @property
    def total_record(self):
        return Record.objects.filter(list=self, status="active").count()

    def __str__(self):
        return self.name


class ListField(models.Model):
    list = models.ForeignKey('List', on_delete=models.SET_NULL, null=True, related_name='list')
    field_id = models.CharField(max_length=10)
    field_label = models.TextField()

    FIELD_TYPE = (
        ('text', 'Text'),
        ('long-text', 'Long Text'),
        ('number', 'Number'),
        ('url', 'Url'),
        ('choose-from-list', 'Choose from List'),
        ('date', 'Date')
        #('choose-multiple-from-list', 'Choose multiple from List'),
    )

    field_type = models.CharField(
        max_length=250,
        choices=FIELD_TYPE,
        blank=False,
        default='text',
    )

    select_list = models.ForeignKey('List', on_delete=models.SET_NULL, null=True, related_name='select_list', blank=True)
    primary = models.BooleanField(null=False, default=False)
    required = models.BooleanField(null=False, default=False)
    visible = models.BooleanField(null=False, default=False)
    order = models.IntegerField(null=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    last_updated = models.DateTimeField(auto_now_add=True)

    LIST_STATUS = (
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('deleted', 'Deleted'),
    )

    status = models.CharField(
        max_length=25,
        choices=LIST_STATUS,
        blank=False,
        default='active',
    )

    def __str__(self):
        return self.field_label

    def save(self, *args, **kwargs):
        self.field_id = str(self.id)
        super(ListField, self).save(*args, **kwargs)


class Record(models.Model):
    list = models.ForeignKey('List', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    last_updated = models.DateTimeField(auto_now_add=True)

    RECORD_STATUS = (
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('deleted', 'Deleted'),
    )

    status = models.CharField(
        max_length=25,
        choices=RECORD_STATUS,
        blank=False,
        default='active',
    )

    @property
    def record_fields(self):
        return RecordField.objects.filter(record=self, status='active', list_field__status="active") \
            .select_related('record__list', 'record__created_user') \
            .select_related('created_user').order_by('list_field__order')

    @property
    def primary_field(self):
        return RecordField.objects.filter(status='active', list_field__primary=True, list_field__status='active') \
            .select_related('record__list', 'record__created_user') \
            .select_related('created_user') \
            .get(record=self)

    def __str__(self):
        return str(self.id)


class RecordField(models.Model):
    record = models.ForeignKey('Record', on_delete=models.SET_NULL, null=True, related_name='record')
    list_field = models.ForeignKey('ListField', on_delete=models.SET_NULL, null=True)
    value = models.TextField(null=True)
    selected_record = models.ForeignKey('Record', on_delete=models.SET_NULL, null=True, related_name='selected_record')
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    last_updated = models.DateTimeField(auto_now_add=True)

    RECORD_FIELD_STATUS = (
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('deleted', 'Deleted'),
    )

    status = models.CharField(
        max_length=25,
        choices=RECORD_FIELD_STATUS,
        blank=False,
        default='active',
    )

    def __str__(self):
        return str(self.id)


class RecordRelation(models.Model):
    parent_record = models.ForeignKey('Record', on_delete=models.SET_NULL, null=True, related_name='parent_record')
    child_record = models.ForeignKey('Record', on_delete=models.SET_NULL, null=True, related_name='child_record')
    list_field = models.ForeignKey('ListField', on_delete=models.SET_NULL, null=True, related_name='list_field')
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    last_updated = models.DateTimeField(auto_now_add=True)

    RECORD_RELATION_TYPE = (
        ('choose-from-list', 'Choose from list'),
        ('embed', 'Embed'),
        ('tag', 'Tag'),
    )

    relation_type = models.CharField(
        max_length=25,
        choices=RECORD_RELATION_TYPE,
        blank=False,
        default='active',
    )

    RECORD_RELATION_STATUS = (
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('deleted', 'Deleted'),
    )

    status = models.CharField(
        max_length=25,
        choices=RECORD_RELATION_STATUS,
        blank=False,
        default='active',
    )

    def __str__(self):
        return str(self.id)

def record_file_path(self, filename):
    new_path = "record" + "/" + str(self.record.pk) + '/'
    return os.path.join(new_path, filename)


class RecordFile(models.Model):
    file = models.FileField(upload_to=record_file_path)
    record = models.ForeignKey(Record,on_delete=models.CASCADE,related_name="files")
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return (str(self.record.list.name) + ' ' + str(self.created_user) )
        
    def filename(self):
        return os.path.basename(self.file.name)

    def url(self):
        if self.file and hasattr(self.file, 'url'):
            return self.file.url
    
    def delete_url(self):
        return reverse('delete_record_file', kwargs={
            'organization_pk':self.record.list.app.organization.pk,
            'list_pk':self.record.list.pk,
            'app_pk':self.record.list.app.pk,
            'record_pk':self.record.pk,
            'record_file_pk':self.pk
            })

def record_media_path(self, filename):
    new_path = "record" + "/media/" + str(self.record.pk) + '/'
    return os.path.join(new_path, filename)

class RecordMedia(models.Model):
    file = models.FileField(upload_to=record_media_path)
    record = models.ForeignKey(Record,on_delete=models.CASCADE,related_name="media")
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return (str(self.record.list.name) + ' ' + str(self.created_user) )
        
    def filename(self):
        return os.path.basename(self.file.name)

    def url(self):
        if self.file and hasattr(self.file, 'url'):
            return self.file.url

    def delete_url(self):
        return reverse('delete_record_media', kwargs={
            'organization_pk':self.record.list.app.organization.pk,
            'list_pk':self.record.list.pk,
            'app_pk':self.record.list.app.pk,
            'record_pk':self.record.pk,
            'record_media_pk':self.pk
            })

class RecordComment(models.Model):
    record = models.ForeignKey(Record,on_delete=models.CASCADE,null=True,blank=True)
    content = models.TextField(default='')
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        content = (self.content[:10] + '..') if len(self.content) > 10 else self.content
        return (content + ' by ' + self.created_user.username +' of #'+ str(self.record.pk))

    def delete_url(self):
        return reverse('delete_record_comment', kwargs={
            'organization_pk':self.record.list.app.organization.pk,
            'list_pk':self.record.list.pk,
            'app_pk':self.record.list.app.pk,
            'record_pk':self.record.pk,
            'record_comment_pk':self.pk
            })


class Note(models.Model):
    note = HTMLField()
    record = models.ForeignKey('Record', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    last_updated = models.DateTimeField(auto_now_add=True)

    NOTE_STATUS = (
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('deleted', 'Deleted'),
    )

    status = models.CharField(
        max_length=25,
        choices=NOTE_STATUS,
        blank=False,
        default='active',
    )

    def __str__(self):
        return self.note
