from django import forms
from .models import Task, Notation

class Task_Form(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['text', 'date']
        labels = {'text': 'Tarefa', 'date': 'data'}
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class Notation_form(forms.ModelForm):
    class Meta:
        model = Notation
        fields = ['text']
        labels = {'text': 'Anotação'}
        widgets = {'text': forms.Textarea(attrs={'cols': 60})}
