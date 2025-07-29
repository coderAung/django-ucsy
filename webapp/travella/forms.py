from django import forms
from .models import Account, AccountDetails, Review, Package, Booking

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['email', 'password', 'type']

class AccountDetailsForm(forms.ModelForm):
    class Meta:
        model = AccountDetails
        fields = ['profile_photo', 'name', 'address', 'phone']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['account', 'content']

class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = '__all__'

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
