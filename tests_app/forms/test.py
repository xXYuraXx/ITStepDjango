from django import forms
from tests_app.models import Test

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['name', 'author', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Test name'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Author'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
            'image': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Image URL'}),
        }