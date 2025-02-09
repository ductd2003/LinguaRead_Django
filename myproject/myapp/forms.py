from django import forms
from .models import Levels, Languages, Postcontent, Questions

class LevelsForm(forms.ModelForm):
    class Meta:
        model = Levels  # Liên kết với model Levels
        fields = ['levelname']  # Chỉ định các trường trong form
        widgets = {
            'levelname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Level Name'
            }),
        }
        labels = {
            'levelname': 'Level Name',
        }

class LanguagesForm(forms.ModelForm):
    class Meta:
        model = Languages
        fields = ['languagename']
        widgets = {
            'languagename': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Language Name'
            }),
        }
        labels = {
            'languagename': 'Language Name',
        }

class PostcontentForm(forms.ModelForm):
    class Meta:
        model = Postcontent
        fields = ['postid', 'languageid', 'levelid', 'title', 'content']
        widgets = {
            'postid': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Post ID'
            }),
            'languageid': forms.Select(attrs={'class': 'form-control'}),
            'levelid': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Content',
                'rows': 5
            }),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['questiontext', 'answer']
