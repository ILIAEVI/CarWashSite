from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from authentication.tokens import generate_token
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from authentication.forms import SignupForm
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model

ACTIVATION_TIMEOUT_MINUTES = 5


def index(request):
    return render(request, 'index.html')


def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate Your CarWash account'
            message = render_to_string('activate_mail.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete registration/t'
                                'You have 5 minutes before the link expires.')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def email_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and generate_token.check_token(user, token):
        if user.date_joined + timedelta(minutes=ACTIVATION_TIMEOUT_MINUTES) < timezone.now():
            user.delete()
            return HttpResponse('Activation link has expired. Please sign up again.')
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    elif user is not None:
        user.delete()
        return HttpResponse('Activation link is invalid! User removed.')
    else:
        return HttpResponse('Activation link is invalid!')


class CustomPasswordResetView(PasswordResetView):
    form_class = PasswordResetForm
    template_name = 'password_reset.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = get_user_model()

        if user.objects.filter(email=email).exists():
            return super().form_valid(form)
        else:
            messages.error(self.request, "This email is not associated with any account.")
            return self.render_to_response(self.get_context_data(form=form))


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            request.session['invalid_login'] = "Invalid Password or username, try again"
            return redirect('login')
    else:
        form = AuthenticationForm
        return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')
