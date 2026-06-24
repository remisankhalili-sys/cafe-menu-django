from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Customer


class CustomerRegistrationForm(UserCreationForm):
    """
    Form for new customer registration.
    Extends Django's built-in UserCreationForm with email and phone number fields.
    """

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'})
    )
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number (optional)'})
    )

    class Meta:
        model = Customer
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm password'})


class CustomerLoginForm(AuthenticationForm):
    """
    Form for customer login.
    Extends Django's built-in AuthenticationForm with Bootstrap styling.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})


class CustomerProfileForm(forms.ModelForm):
    """
    Form for updating customer profile information.
    Allows customers to update their username, email, phone number and profile picture.
    """

    class Meta:
        model = Customer
        fields = ['username', 'email', 'phone_number', 'profile_picture']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }