from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic, View
from django.urls import reverse_lazy
from .forms import SignUpForm, UpdateProfileForm, UpdatePasswordForm
from django.contrib.auth.models import User


class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


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
