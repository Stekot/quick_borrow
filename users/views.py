from django.contrib.auth.views import LoginView as LoginViewBase, LogoutView as LogoutViewBase


class LoginView(LoginViewBase):
    template_name = 'login.html'
    redirect_authenticated_user = True
    success_url = ''


class LogoutView(LogoutViewBase):
    template_name = 'logout.html'
    success_url = ''