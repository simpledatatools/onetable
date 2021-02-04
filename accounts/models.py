from django.db import models
from django.contrib.auth.models import User


class MailLinkModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    key = models.CharField(max_length=255, default="", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False, null=True, blank=True)

    link_type_choice = (
        ('sign_up', 'SignUp'),
        ('reset_password', 'Reset Password'),
    )

    link_type = models.CharField(max_length=100, default="", choices=link_type_choice, null=True, blank=True)

    def __str__(self):
        return self.user.email
