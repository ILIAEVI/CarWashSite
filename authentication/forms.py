from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    email = forms.EmailField(help_text="Enter your Email Address")
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def clean_email(self):
        current_email = self.cleaned_data.get('email')
        if User.objects.filter(email=current_email).exists():
            raise forms.ValidationError("This email address is already used")
        return current_email

