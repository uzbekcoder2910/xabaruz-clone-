from django.forms import ModelForm
from django import forms
from .models import Contact, Comment


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name*'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email*'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Message*', 'rows': 5}),
        }


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ['body']