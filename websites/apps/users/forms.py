from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    A custom form for creating new users that includes all the required
    fields, plus any additional fields on your custom user model.
    """
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'first_name', 'last_name')
        # You can customize field labels or widgets if needed.
        labels = {
            'username': 'Username',
            'email': 'Email Address',
            'role': 'User Role',
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }

class CustomUserChangeForm(UserChangeForm):
    """
    A custom form for updating users. Includes all the fields on the user,
    but replaces the password field with admin's password hash display field.
    """
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'first_name', 'last_name', 'bio', 'profile_picture')
        labels = {
            'username': 'Username',
            'email': 'Email Address',
            'role': 'User Role',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'bio': 'Biography',
            'profile_picture': 'Profile Picture',
        }
