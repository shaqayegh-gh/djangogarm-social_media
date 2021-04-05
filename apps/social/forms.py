import phonenumbers as phonenumbers
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models.profile import Post
from .models.user import User


class RegisterFrom(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'username']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        z = phonenumbers.parse("+98{}".format(phone_number), None)  # install phonenumbers
        if not phonenumbers.is_valid_number(z):
            raise forms.ValidationError("Number not in correct format")
        return z.national_number


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption', 'photo']
