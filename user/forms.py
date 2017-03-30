#-*- coding: utf-8 -*-
from django.contrib.auth.models import User

from django.db import models

from django import forms

from django.core import validators

from django.core.validators import EmailValidator,ValidationError

from django.template import Context,Template

from django.core.mail import EmailMultiAlternatives

from django.conf import settings

from user.models import Profile

import datetime

from django.forms.utils import ErrorList


class UserLoginForm(forms.ModelForm):
    password = forms.CharField( widget=forms.PasswordInput( attrs={'placeholder': 'Hasło'} ) )
    username = forms.CharField( widget=forms.TextInput( attrs={'placeholder': 'Nazwa użytkownika'} ) )
    class Meta:
        model = User # Uzyj modelu User
        fields = ['username','password']

def isValidUsername(field_data): # Validator dla nazy uzytwkonika. Czy juz istnieje.
    try:
        User.objects.get(username=field_data)
    except User.DoesNotExist:
        return
    raise validators.ValidationError('Nazwa użytkownika \'{}\' jest zajęta.'.format(field_data) )

class RegistrationForm(forms.Form):
    username = forms.CharField(
                                label="",
                                widget=forms.TextInput(attrs={'placeholder': 'Nazwa użytkownika','class':'form-control input-perso'}),
                                max_length=30,
                                min_length=3,
                                validators=[isValidUsername, validators.validate_slug]
                            )

    email = forms.EmailField(
                                label="",
                                widget=forms.EmailInput(attrs={'placeholder': 'E-mail','class':'form-control input-perso'}),
                                max_length=100,
                                error_messages={'invalid': ("Adres e-mail jest w niepoprawnym formacie.")},
                                validators=[EmailValidator]
                            )

    password1 = forms.CharField(
                                label="",
                                max_length=50,
                                min_length=6,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Hasło użytkownika','class':'form-control input-perso'})
                            )

    password2 = forms.CharField(
                                label="",
                                max_length=50,
                                min_length=6,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Potwierdź hasło','class':'form-control input-perso'})
                            )

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password1 != password2:
            self._errors['password2'] = ErrorList(["Wpisane hasła nie są takie same."])

        return self.cleaned_data

    def save(self, datas):
        u = User.objects.create_user(datas['username'],datas['email'],datas['password1'])
        u.is_active = False
        u.save()

        profile=Profile.objects.get(user__username=datas['username'])
        profile.activation_key=datas['activation_key']
        profile.key_expires=datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
        profile.save()
        return u

    def sendEmail(self, datas):
        link = "http://pycity.com/user/activate/"+datas['activation_key']

        c = Context( {'activation_link':link,'username':datas['username']} )

        f = open( 'user/static'+datas['email_path'], 'r' )
        t = Template( f.read().encode('utf8') )
        f.close()

        message = t.render(c)

        subject = 'PyCity - Aktywuj swoje konto!'
        from_email = '{}'.format( settings.EMAIL_HOST_USER )
        to = datas['email']
        text_content = 'Dziękujemy za rejestrację. Wciśnij ten link aby aktywować swoje konto : {}'.format( link )
        html_content = message

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
