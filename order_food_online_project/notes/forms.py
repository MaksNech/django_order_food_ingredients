from django import forms
from .models import Note


class NoteAddForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'description']
