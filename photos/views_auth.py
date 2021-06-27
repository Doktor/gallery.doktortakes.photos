from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.decorators.http import require_GET

from photos.forms import RegisterForm


class LogInView(View):
    template_name = 'log_in.html'

    action = None
    next_url = None

    def dispatch(self, request, *args, **kwargs):
        next_url = request.GET.get('next', reverse('index'))

        action = f"{reverse('log_in')}"
        if next_url != '/':
            action += f"?next={next_url}"

        self.next_url = next_url
        self.action = action

        if request.user.is_authenticated:
            return redirect(self.next_url)

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {
            'action': self.action,
            'register': getattr(settings, "ENABLE_REGISTRATION", False),
        }

        return render(request, self.template_name, context)

    def post(self, request):
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            context = {
                'action': self.action,
            }

            messages.error(request, "Invalid username or password.")
            return render(request, self.template_name, context)

        login(request, user)
        messages.success(request, "Logged in successfully.", extra_tags='fade')

        return redirect(self.next_url)


@require_GET
@login_required
def log_out(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out successfully.", extra_tags='fade')

    return redirect('index')


class RegisterView(View):
    form_class = RegisterForm
    template_name = 'register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            get_user_model().objects.create_user(
                username, email=email, password=password)

            user = authenticate(username=username, password=password)

            login(request, user)
            messages.success(request, "Account created successfully.", extra_tags='fade')
            return redirect('index')
        else:
            messages.error(request, "Please fix the errors below.")
            return render(request, self.template_name, {'form': form})
