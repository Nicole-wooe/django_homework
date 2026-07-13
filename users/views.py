from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import UserLoginForm, UserRegisterForm


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        response = super().form_valid(form)

        send_mail(
            subject="Добро пожаловать!",
            message="Спасибо за регистрацию в нашем интернет-магазине.",
            from_email=None,
            recipient_list=[self.object.email],
            fail_silently=True,
        )

        return response


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "users/login.html"


class UserLogoutView(LogoutView):
    pass
