from django import forms
from travella.domains.models.tour_models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data['name']
        if Category.objects.filter(name=name).exists():
            raise forms.ValidationError("Category with this Name already exists.")
        return name
