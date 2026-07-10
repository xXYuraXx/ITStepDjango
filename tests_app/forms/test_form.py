from django import forms
from tests_app.models import Test

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['name', 'author', 'description', "genre", 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Test name'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
            'genre': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Image'}),  
        }