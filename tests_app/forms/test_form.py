from django import forms
from tests_app.models import Test, Question, Option


class TestBaseForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['name', 'description', 'genre', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Test name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
            'genre': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Image'}),
        }


class TestStaffForm(TestBaseForm):
    class Meta(TestBaseForm.Meta):
        model = Test
        fields = ['name', 'author', 'description', 'genre', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Test name'}),
            'author': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
            'genre': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Image'}),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_type', 'question_text', 'correct_val', 'correct_text']
        widgets = {
            'question_type': forms.Select(attrs={'class': 'form-select question-type-select'}),
            'question_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Question text'}),
            'correct_val': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Points'}),
            'correct_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Correct text answer'}),
        }


class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['text', 'is_correct', 'match_text']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Option text'}),
            'is_correct': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'match_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Matching pair text'}),
        }


QuestionFormSet = forms.inlineformset_factory(Test, Question, form=QuestionForm, extra=1, can_delete=True)

OptionFormSet = forms.inlineformset_factory(Question, Option, form=OptionForm, extra=1, can_delete=True)