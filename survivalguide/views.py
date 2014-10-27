from django.contrib.auth import (
    authenticate,
    login,
    logout
)
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.views.generic import (
    TemplateView,
    CreateView,
    FormView
)
from django.http import HttpResponseRedirect

from .forms import RegistrationForm, LoginForm


class HomePageView(TemplateView):
    template_name = 'home.html'


class SignUpView(CreateView):
    form_class = RegistrationForm
    model = User
    template_name = 'accounts/signup.html'


class LoginView(FormView):
    form_class = LoginForm
    success_url = reverse_lazy('home')
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('home'))
