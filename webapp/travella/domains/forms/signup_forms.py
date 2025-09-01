from django import forms
from django.core.exceptions import ValidationError

# Common attributes for form widgets
common_attrs = {'class': 'form-control'}

class Step1Form(forms.Form):
    full_name = forms.CharField(max_length=100, required=True, label="Full Name",
        widget=forms.TextInput(attrs={**common_attrs, 'placeholder': 'Enter your full name'}))
    email = forms.EmailField(required=True, label="Email Address",
        widget=forms.EmailInput(attrs={**common_attrs, 'placeholder': 'Enter your email address'}))
    password = forms.CharField(required=True, label="Password",
        widget=forms.PasswordInput(attrs={**common_attrs, 'placeholder': 'Enter a strong password'}))
    confirm_password = forms.CharField(required=True, label="Confirm Password",
        widget=forms.PasswordInput(attrs={**common_attrs, 'placeholder': 'Confirm your password'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data

class Step2Form(forms.Form):
    phone_number = forms.CharField(max_length=20, required=False, label="Phone Number (Optional)",
        widget=forms.TextInput(attrs={**common_attrs, 'placeholder': 'Enter Your Phone Number'}))
    address = forms.CharField(required=False, label="Address (Optional)",
        widget=forms.Textarea(attrs={**common_attrs, 'rows': 3, 'placeholder': 'Your current address'}))

class Step3Form(forms.Form):
    profile_photo = forms.ImageField(required=False, label="Profile Photo (Optional)",
        widget=forms.FileInput(attrs={'class': 'file-upload-input', 'onchange': 'updateFileName(this)'}))