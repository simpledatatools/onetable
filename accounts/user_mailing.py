from django.core.mail import send_mail
from django.conf import settings
import string
import random


def create_link(link_for: str):
    choice = string.ascii_letters + string.digits
    key = "".join(random.choice(choice) for _ in range(30))
    if link_for == 'sign-up':
        link = f"{settings.BASE_URL}create-account?key={key}"
    elif link_for == 'reset-password':
        link = f"{settings.BASE_URL}forgot-password?key={key}"
    return link, key


class SendUserMail:
    def __init__(self, recipient_name: str, link: str, recipient_list: list, subject: str, mail_for: str):
        self.recipient_name = recipient_name
        self.link = link
        self.from_email = settings.EMAIL_HOST_USER
        self.recipient_list = recipient_list
        self.subject = subject

        if mail_for == "sign-up":
            self.content = self.__sign_up_compose_mail()
        elif mail_for == "reset-password":
            self.content = self.__reset_password_compose_mail()

    def __sign_up_compose_mail(self):
        content = f"""
        Hello {self.recipient_name.title()},\n
        Thanks so much for signing up for OneTable!\n
        Use the link below to confirm your account:\n
        {self.link}\n
        If you didn't sign up for OneTable, please ignore this email.\n
        Sincerely,\n
        OneTable Support
        """
        return content

    def __reset_password_compose_mail(self):
        content = f"""
        Hello {self.recipient_name.title()},\n
        We received a request to change the password for the account with the email {self.recipient_list}\n
        Use the link below to reset your password:\n
        {self.link}\n
        If you don't want to reset your password or you did not request this change, you can ignore this email.\n
        Sincerely,\n
        OneTable Support
        """
        return content

    def send(self):
        try:
            send_mail(subject=self.subject, message=self.content, from_email=self.from_email, recipient_list=[self.recipient_list], fail_silently=True)
            return True
        except Exception:
            return False
