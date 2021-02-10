from django.contrib import admin
from .models import MailLinkModel


class MailLinkModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_email', 'key', 'created_at', 'link_type', 'is_delete']

    def user_email(self, obj):
        return obj.user.email


admin.site.register(MailLinkModel, MailLinkModelAdmin)
