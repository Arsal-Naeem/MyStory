from dataclasses import field
from django import forms  
from django.contrib.auth.models import User  
from django.contrib.auth.forms import UserCreationForm  
from django.core.exceptions import ValidationError
from django.forms import ModelForm  
from django.forms.fields import EmailField  
from django.forms.forms import Form
from .models import Story  
  

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label="First name", min_length=3, max_length=150)
    last_name = forms.CharField(label='Last name', min_length=3, max_length=150) 
    username = forms.CharField(label='Username', min_length=5, max_length=150)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput) 
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)  

    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = User.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("User Already Exist")  
        return username  

  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2  


    def save(self, commit = True):  
        user = User.objects.create_user(  
            self.cleaned_data['username'],
            None,
            self.cleaned_data['password1'],
            first_name = self.cleaned_data['first_name'],
            last_name = self.cleaned_data['last_name']
        )  
        return user

    
class storyForm(ModelForm):
    class Meta:
        model = Story
        exclude = ['user']
        widgets = {
            'Story': forms.Textarea(attrs={
            'style': 'resize: none;',
            'class': 'editor',
            'placeholder': 'Story goes here...'})
         }