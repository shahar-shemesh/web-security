from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password, check_password
from Comunication_LTD.models import NS_user

from django.core.exceptions import ValidationError

# Import custom user model
from django.contrib.auth import get_user_model

class UserLoginForm(ModelForm):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(make_password(self.cleaned_data["password1"]))
        if commit:
            user.save()
        return user



#check_password(password, encoded, setter=None, preferred='default')

# class QuickCreateForm(ModelForm):
#     username = forms.CharField(label='Username', max_length=150)
#     email = forms.EmailField(label='E-Mail')
#     password = forms.CharField(label='Password', widget=forms.PasswordInput)
#
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']


class QuickCreateForm(ModelForm):
    username = forms.CharField(label='Username')
    email = forms.CharField(label='Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    #password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1')

    # def clean_password2(self):
    #     # Check that the two password entries match
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         raise ValidationError("Passwords don't match")
    #     return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

        return user



class NOT_SC_UserLoginForm(ModelForm):
    username = forms.CharField()
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    class Meta:
        model = NS_user
        fields = ('username', 'password')


class NOT_SC_UserRegisterForm(ModelForm):
    username = forms.CharField(label='Username')
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # def clean_password2(self):
    #     # Check that the two password entries match
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         raise ValidationError("Passwords don't match")
    #     return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user



class NOT_SC_QuickCreateForm(ModelForm):
    username = forms.CharField(label='Username')
    email = forms.CharField(label='Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = NS_user
        fields = ('username', 'email', 'password1')

    def save(self, commit=True):
        #user = super().save(commit=False)
        user = User.objects.create_user(self.username, self.email,self.password1,self.password1)
        #user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

        return user
