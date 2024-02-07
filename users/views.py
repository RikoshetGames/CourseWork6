from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
from users.forms import RegisterForm, ModeratorForm
from users.models import User
from django.utils.crypto import get_random_string
from django.contrib.auth import logout


class UserLoginView(LoginView):
    template_name = 'users/login.html'


def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('users:login'))

class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'users/register.html'

    def form_valid(self, form):
        self.object = form.save()
        self.object.is_active = False
        self.object.verify_code = get_random_string(12)
        self.object.save()
        url = f'http://127.0.0.1:8000/users/email/verify/{self.object.verify_code}'
        send_mail(
                subject='Регистрация',
                message=f'Для успешной регистрации перейдите по ссылке: {url}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[self.object.email],
                fail_silently=False,
            )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('users:verify_message')


def verification(request, verify_code):
    try:
        user = User.objects.filter(verify_code=verify_code).first()
        user.is_active = True
        user.save()
        return redirect('users:success_verify')
    except (AttributeError, ValidationError):
        return redirect('users:invalid_verify')


class UserUpdateView(PermissionRequiredMixin, UpdateView):
    model = User
    form_class = ModeratorForm
    permission_required = 'set_is_active'
    success_url = 'users:users_list'

    def get_success_url(self):
        return reverse('users:list_view')


@login_required
@permission_required(['users.view_user', 'users.set_is_active'])
def get_users_list(request):
    users_list = User.objects.all()
    context = {
        'object_list': users_list,
        'title': 'Список пользователей сервиса',
    }
    return render(request, 'users/users_list.html', context)
