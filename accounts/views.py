from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic, View
from django.urls import reverse_lazy
from .forms import SignUpForm, UpdateProfileForm, UpdatePasswordForm, UserLoginForm, UserPasswordResetForm, UserSetPasswordForm
from django.contrib.auth.models import User
from .user_mailing import create_link, SendUserMail
from .models import MailLinkModel
from django.contrib.auth import authenticate, login


class LoginView(View):
    template_name = 'registration/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('organizations')
        else:
            form = UserLoginForm()
            return render(request, self.template_name, locals())

    def post(self, request):
        form = UserLoginForm(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = get_object_or_404(User, email=email)
        if user.is_active:
            auth_obj = authenticate(request=request, username=user.username, password=password)
            if auth_obj:
                login(request, auth_obj)
                return redirect('organizations')
            else:
                password_invalid = True
                return render(request, self.template_name, locals())
        else:
            return render(request, self.template_name, locals())


class UserRegistrationView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'registration/register.html', locals())

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_email = user.email
            user_name = user.get_full_name()
            link, key = create_link(link_for='sign-up')
            obj, created = MailLinkModel.objects.update_or_create(user=user, link_type="sign_up", is_delete=False)
            obj.key = key
            obj.save()
            mail = SendUserMail(recipient_name=user_name, link=link, recipient_list=user_email, subject="Complete OneTable Sign Up", mail_for="sign-up")
            status = mail.send()
            context = {'email': user_email, 'render_kind': 'signup'}
            return render(request, 'signup_thankyou_page.html', context)
        else:
            return render(request, 'registration/register.html', locals())


class UserProfileView(View):
    template_name = 'registration/profile.html'

    def get(self, request):
        user_object = get_object_or_404(User, pk=request.user.id)
        form = UpdateProfileForm(instance=user_object)
        return render(request, self.template_name, locals())

    def post(self, request):
        user_object = get_object_or_404(User, pk=request.user.id)
        form = UpdateProfileForm(data=request.POST, instance=user_object)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, self.template_name, locals())


class UpdateProfilePassword(View):
    template_name = 'registration/update_password.html'

    def get(self, request):
        user_object = get_object_or_404(User, pk=request.user.id)
        form = UpdatePasswordForm(user=user_object)
        return render(request, self.template_name, locals())

    def post(self, request):
        user_object = get_object_or_404(User, pk=request.user.id)
        form = UpdatePasswordForm(data=request.POST, user=user_object)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, self.template_name, locals())


class VerifyUserLinkView(View):
    def get(self, request):
        get_key = request.GET.get('key')
        link_obj = get_object_or_404(MailLinkModel, key=get_key)
        if link_obj:
            if link_obj.is_delete is False:
                user = get_object_or_404(User, pk=link_obj.user_id)
                if link_obj.link_type == 'sign_up':
                    user.is_active = True
                    user.save()
                    link_obj.is_delete = True
                    link_obj.save()
                    return render(request, 'signup_thankyou_page.html', {'render_kind': 'signup_confirmed'})
                elif link_obj.link_type == 'reset_password':
                    request.session['forgot_password_user_pk'] = user.pk
                    request.session['forgot_password_link_pk'] = link_obj.pk
                    return redirect('create_new_password')
        return render(request, 'signup_thankyou_page.html', {'render_kind': 'invalid_key'})


class ResetPasswordView(View):
    template_name = 'password_reset_form.html'

    def get(self, request):
        form = UserPasswordResetForm()
        return render(request, self.template_name, locals())

    def post(self, request):
        email = request.POST.get('email')
        user = get_object_or_404(User, email=email)

        if user:
            if user.is_active:
                user_email = user.email
                user_name = user.get_full_name()
                link, key = create_link(link_for='reset-password')
                obj, created = MailLinkModel.objects.update_or_create(user=user, link_type="reset_password", is_delete=False)
                obj.key = key
                obj.save()
                mail = SendUserMail(recipient_name=user_name, link=link, recipient_list=user_email, subject="Reset your OneTable password", mail_for="reset-password")
                status = mail.send()
                context = {'email': user_email, 'render_kind': 'reset_password'}
                return render(request, 'signup_thankyou_page.html', context)
        return self.get(request)


class CreateNewPasswordView(View):
    template_name = 'password_reset_confirm.html'

    def get(self, request):
        user_pk = request.session.get('forgot_password_user_pk')
        user = get_object_or_404(User, pk=user_pk)
        form = UserSetPasswordForm(user=user)
        return render(request, self.template_name, locals())

    def post(self, request):
        user_pk = request.POST.get('user_id')
        user = get_object_or_404(User, pk=user_pk)
        form = UserSetPasswordForm(data=request.POST, user=user)
        if form.is_valid():
            form.save()
            request.session.pop('forgot_password_user_pk')
            link_obj_pk = request.session.get('forgot_password_link_pk')
            link_obj = get_object_or_404(MailLinkModel, pk=link_obj_pk)
            link_obj.is_delete = True
            link_obj.save()
            request.session.pop('forgot_password_link_pk')
        else:
            return render(request, self.template_name, locals())
        return render(request, 'signup_thankyou_page.html', {'render_kind': 'password_updated'})
