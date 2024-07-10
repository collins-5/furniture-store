from django import forms
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm as AuthPasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User

from dashboard.models import Post

class loginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'enter Your username',
        'class': 'w-full py-4  px-6 rounded-xl'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'enter your password',
        'class': 'w-full  py-4 px-6 rounded-xl'
    }))

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('FirstName','SecondName','username', 'email', 'password1', 'password2')
    FirstName = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter First Nname',
        'class': 'w-full  py-1 px-7 rounded-xl'
    })) 
    SecondName = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Second Nname',
        'class': 'w-full py-1  px-6 rounded-xl'
    }))   
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'w-full py-1  px-6 rounded-xl'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your email',
        'class': 'w-full py-1 px-6  rounded-xl'
    }))  
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'create password',
        'class': 'w-full py-1 px-6  rounded-xl'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'confirm password',
        'class': 'w-full py-1 px-6 rounded-xl'
    }))      
class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full py-4 px-6 rounded-xl', 'placeholder': 'Title'}),
            'content': forms.Textarea(attrs={'class': 'w-full py-4 px-6 rounded-xl', 'placeholder': 'Content'}),
        }
class PasswordResetForm(AuthPasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your email',
        'class': 'w-full py-4 px-6 bg-transparent rounded-xl'
    }))

class SetNewPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'New password',
        'class': 'w-full py-4 px-6 bg-transparent rounded-xl'
    }))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm new password',
        'class': 'w-full py-4 px-6 bg-transparent rounded-xl'
    }))