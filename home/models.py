from django.db import models
from django.conf import settings
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone
from django.db.models import JSONField
import os
from django.conf import settings
from django.db import models
from imagekit.processors import ResizeToFit
from imagekit.models import ImageSpecField
from .utils import save_frame_from_video
import string 
import random 
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver



class Organization(models.Model):
    id = models.CharField(primary_key=True, default='', editable=False,max_length=10)
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    active_users = models.ManyToManyField(User,through="OrganizationUser",through_fields=( 'organization','user'))
    inactive_users = models.ManyToManyField('InactiveUsers')
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
    
    def membersCount(self):
        active_users = OrganizationUser.objects.filter(organization=self,status="active").count()
        inactive_users = self.inactive_users.all().count()
        return active_users + inactive_users

    #memberscount = property(MembersCount)

    def __str__(self):
        return self.name
        
    
    
class OrganizationUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    created = models.BooleanField(default=False)
    permitted_apps = models.ManyToManyField('App')
    can_access_all_apps = models.BooleanField(default=False)

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

    def __str__(self):
        return self.organization.name + ' - ' + self.user.username

# class App(models.Model):
#     id = models.CharField(primary_key=True, default='', editable=False,max_length=10)

#     name = models.CharField(max_length=200)
#     description = models.TextField()
#     organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True)
#     created_at = models.DateTimeField(auto_now_add=True, null=False)
#     created_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
#     last_updated = models.DateTimeField(auto_now_add=True)

#     APP_STATUS = (
#         ('active', 'Active'),
#         ('archived', 'Archived'),
#         ('deleted', 'Deleted'),
#     )

#     status = models.CharField(
#         max_length=25,
#         choices=APP_STATUS,
#         blank=False,
#         default='active',
#     )

#     # TODO add @property for app users

#     def __str__(self):
#         return self.name



class App(models.Model):
    id = models.CharField(primary_key=True, default='', editable=False,max_length=10)
    name = models.CharField(max_length=200)
    description = models.TextField()
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    last_updated = models.DateTimeField(auto_now_add=True)
    app_level_users = models.ManyToManyField(User,through="AppUser",through_fields=( 'app','user'))
    inactive_users = models.ManyToManyField('InactiveUsers')

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
    
    def __str__(self):
        return self.name

    def membersCount(self):
        active_users = OrganizationUser.objects.filter(organization = self.organization,status='active',permitted_apps = self).count()
        inactive_users = InactiveUsers.objects.filter(attached_workspaces = self).count()
        return active_users + inactive_users

class AppUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    app = models.ForeignKey('App', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    created = models.BooleanField(default=False)
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
    id = models.CharField(primary_key=True, default='', editable=False,max_length=10)
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
    id = models.CharField(primary_key=True, default='', editable=False,max_length=10)
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
    id = models.CharField(primary_key=True, default='', editable=False,max_length=10)
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
    id = models.CharField(primary_key=True, default='', editable=False,max_length=10)
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
    id = models.CharField(primary_key=True, default='', editable=False,max_length=10)
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
    id = models.CharField(primary_key=True, default='', editable=False,max_length=10)
    file = models.FileField(upload_to=record_file_path)
    record = models.ForeignKey(Record,on_delete=models.CASCADE,related_name="files")
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    name_of_file = models.CharField(max_length=200,default='')
    file_extension = models.CharField(max_length=200,default='')

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

    def edit_url(self):
        return reverse('edit_record_file', kwargs={
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
    id = models.CharField(primary_key=True, default='', editable=False,max_length=10)
    file = models.FileField(upload_to=record_media_path)
    record = models.ForeignKey(Record,on_delete=models.CASCADE,related_name="media")
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    image_types = ['image/jpeg', 'image/gif', 'image/png']
    video_types = ['video/mp4', 'video/x-matroska',
                               'video/ogg','video/quicktime', 'video/x-ms-wmv',
                               'video/webm']

    IMAGE = 'I'
    VIDEO = 'V'
    TYPES = [
        (IMAGE, 'Image'),
        (VIDEO, 'Video'),
    ]
    thumbnail_millisecond = models.IntegerField(default=0)
    type = models.CharField(max_length=1, choices=TYPES, blank=True)
    thumbnail_source_image = models.ImageField(upload_to='post_files/%Y/%m/%d/', null=True, blank=True)
    image_thumbnail = ImageSpecField(source='thumbnail_source_image',
                                     processors=[
                                         ResizeToFit(300,
                                                     300,
                                                     mat_color=(230, 230, 230)),
                                     ],
                                     format='JPEG',
                                     options={'quality': 95})

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

    def _set_type(self):
        # max bytes to read for file type detection
        read_size = 500 * (1024 * 1024)  # 5MB

        # read mime type of file
        from magic import from_buffer
        mime = from_buffer(self.file.read(read_size), mime=True)

        if mime in self.image_types:
            self.type = self.IMAGE
        elif mime in self.video_types:
            self.type = self.VIDEO

    def _set_thumbnail_source_image(self):
        if self.type == self.IMAGE:
            self.thumbnail_source_image = self.file
        elif self.type == self.VIDEO:
            # create thumbnail source file
            image_path = os.path.splitext(self.file.path)[0] + '_thumbnail_src_image.jpg'
            save_frame_from_video(self.file.path, int(self.thumbnail_millisecond), image_path)

            # generate path relative to media root, because this is the version that ImageField accepts
            media_image_path = os.path.relpath(image_path, settings.MEDIA_ROOT)

            self.thumbnail_source_image = media_image_path

    def save(self, *args, **kwargs):
        if self.type == '':
            self._set_type()
        # if there is no source image
        if not bool(self.thumbnail_source_image):
            # we need to save first, for django to generate path for file in "file" field
            super().save(*args, **kwargs)
            self._set_thumbnail_source_image()

        super().save(*args, **kwargs)


class RecordComment(models.Model):
    id = models.CharField(primary_key=True, default='', editable=False,max_length=10)
    record = models.ForeignKey(Record,on_delete=models.CASCADE,null=True,blank=True)
    content = models.TextField(default='')
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        content = (self.content[:10] + '..') if len(self.content) > 10 else self.content
        return (content + ' by ' + self.created_user.username +' of #'+ str(self.record.pk))
    
    def edit_url(self):
        return reverse('edit_record_comment', kwargs={
            'organization_pk':self.record.list.app.organization.pk,
            'list_pk':self.record.list.pk,
            'app_pk':self.record.list.app.pk,
            'record_pk':self.record.pk,
            'record_comment_pk':self.pk
            })

    def delete_url(self):
        return reverse('delete_record_comment', kwargs={
            'organization_pk':self.record.list.app.organization.pk,
            'list_pk':self.record.list.pk,
            'app_pk':self.record.list.app.pk,
            'record_pk':self.record.pk,
            'record_comment_pk':self.pk
            })



class Note(models.Model):
    id = models.CharField(primary_key=True, default='', editable=False,max_length=10)
    note = models.TextField()
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



class InactiveUsers(models.Model):
    user_email = models.EmailField(null=True)
    #attached_organizations = models.ManyToManyField(Organization)
    created_at = models.DateTimeField(auto_now_add=True)
    attached_workspaces= models.ManyToManyField(App,related_name='apps')
    #attached_workspaces = models.ManyToManyField(App)

    def __str__(self):
        return self.user_email


@receiver(post_save, sender=User)
def update_stock(sender, instance, **kwargs):
    inactive_user = InactiveUsers.objects.filter(user_email=instance.email).exists()
    if inactive_user==True:
        inactive_user= InactiveUsers.objects.get(user_email=instance.email)
        att_orgs = inactive_user.organization_set.all()
        for org in att_orgs:
            org.active_users.add(instance)
        #instance.active_users.add(att_orgs)
        att_workspaces = inactive_user.attached_workspaces.all()
        for wrksps in att_workspaces:
            org = Organization.objects.get(id = wrksps.organization.pk)
            org.active_users.add(instance)
            org.save()
            org_user = OrganizationUser.objects.get_or_create(user=instance,organization_id = wrksps.organization.pk)
            org_user[0].permitted_apps.add(wrksps)
            org_user[0].save()
        inactive_user.delete()