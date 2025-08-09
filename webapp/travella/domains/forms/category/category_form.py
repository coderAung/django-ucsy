from django import forms
from travella.domains.models.tour_models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']  # Only include the fields you want to expose in the form
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name',
                'required': 'required'
            }),
        }
