from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout

from django.template.context_processors import media
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from .forms import UserLoginForm, RegistrationForm
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic import View
from django.http import HttpResponse
from django.utils import timezone
from django.views import generic
from .models import Profile

from django.contrib.auth.decorators import login_required

import hashlib
import random
import datetime
import re
import string

from tutorials.views import nav

from django.utils.translation import ugettext as _


class Login(View):
    form_class = UserLoginForm
    template_name = 'user/login.html'

    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponse('Jesteś już zalogowany. Wyloguj się, aby przelogować się na inne konto. <a href="../../">Strona główna</a> ')
        form = self.form_class(None)
        request_auth_error = request.GET.get('auth_error', '')
        request_next = request.GET.get('next', '')

        if request_next == None or request_next == '':
            request_next = 'Profile'

        return render(request, self.template_name, {
            'form': form,
            'title': 'Zaloguj się',
            'request_auth_error': request_auth_error,
            'request_next': request_next,
        })

    def post(self, request):
        if request.POST:
            try:
                username = request.POST['username']
                password = request.POST['password']
                next_ = request.POST['next']
                user = authenticate(username=username, password=password)
            except:
                return HttpResponse('Authentication failure')  # Profilaktyczny except

            if user is not None:
                if user.is_active:
                    login(request,user)
                    try:
                        return redirect(next_)  # Pomyślne logowanie
                    except:
                        return redirect('Profile')

        return redirect('./?auth_error=1')  # Niepomyślne logowanie


def logoutUser(request):  # Wylogowanie
    logout(request)
    return redirect('home')


def register(request):
    if request.user.is_authenticated():  # Przenieś do strony głównej jeśli zalogowany
        return redirect('home')

    registration_form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():

            datas = {}
            datas['username']=form.cleaned_data['username']
            datas['email']=form.cleaned_data['email']
            datas['password1']=form.cleaned_data['password1']

            # Czy na tym adresie email zalozono juz konto
            try:
                already_exist = User.objects.get(email=datas['email'])
                return HttpResponse('Konto o adresie "{}" już istnieje. <a href="./">Wróć do rejestracji</a>'.format( datas['email'] ))
            except:
                pass

            # Tworzenie klucza aktywacyjnego na podstawie: salt+użytkownik
            salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:5]
            usernamesalt = datas['username'].encode('utf-8')
            buffor = '{}{}'.format(salt, usernamesalt)

            datas['activation_key'] = hashlib.sha1(buffor.encode('utf-8')).hexdigest()
            datas['email_path'] = "/ActivationEmail.html"

            form.sendEmail(datas)
            form.save(datas)

            # Zapamiętanie id uzytkownika dla funkcji new_activation_link()
            request.session['resend_id'] = form.cleaned_data

            return redirect('thanks')
        else:
            registration_form = form
    return render(request, 'user/registration.html', locals())


def activation(request, key):  # Aktywacja
    activation_expired = False
    already_active = False
    profile = get_object_or_404(Profile, activation_key=key)
    if not profile.user.is_active:
        if timezone.now() > profile.key_expires:
            request.session['resend_id'] = {'username': profile.user.username}
            activation_expired = True
            id_user = profile.user.id
        else:

            profile.user.is_active = True
            profile.user.save()

    else:
        already_active = True
    return render(request, 'user/activation.html', locals())


def thanks_for_reg(request):  # Podziękowanie za rejestrację
    try:
        c_user = request.session['resend_id']['username']
        context = User.objects.get(username=c_user).id
    except:
        return HttpResponse(' ')
    return render( request, 'user/thanks.html', {'context': context})


def new_activation_link(request, user_id):  # Ponowne wysłanie linka aktywującego
    form = RegistrationForm()
    datas = {}

    user = User.objects.get(id=user_id)

    if user is not None and not user.is_active:
        datas['username'] = user.username
        datas['email'] = user.email
        datas['email_path'] = "/ActivationEmail.html"
        datas['email_subject'] = "Resended actv email"

        salt = hashlib.sha1( str(random.random()).encode('utf8') ).hexdigest()[:5]
        usernamesalt = datas['username'].encode('utf-8')
        buffor = '{}{}'.format( salt,usernamesalt)
        datas['activation_key']= hashlib.sha1( buffor.encode('utf-8') ).hexdigest()

        profile = Profile.objects.get(user__username=datas['username'])
        profile.activation_key = datas['activation_key']
        profile.key_expires = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
        profile.save()

        form.sendEmail(datas)
    else:
        return HttpResponse('To konto jest już aktywne.<a href="../../../">Strona główna</a>')

    return redirect('thanks')


@login_required(login_url='/user/login')
def profile(request):
    datas = {}
    idict = nav(request)
    datas['user'] = request.user
    title = 'Profile - {}'.format( request.user.username )

    if request.user.is_authenticated() == False:
        return redirect('home')
    else:
        return render(request, 'user/profile.html',
            {
                "datas": datas,
                "idict":idict,
                'title':title,
            })


def sendEmail(email, key):
    from django.template import Context, Template
    from django.core.mail import EmailMultiAlternatives
    from django.conf import settings
    link = "http://pycity.com/user/passreset/{}/".format(key)
    c = Context({'activation_link': link})
    f = open('user/static/ForgottenPassword.html', 'r')

    t = Template(f.read().encode('utf8'))
    f.close()
    message = t.render(c)
    subject = 'PyCity  Zresetuj hasło'
    from_email = '{}'.format(settings.EMAIL_HOST_USER)
    to = email
    text_content = "Aby zresetować swoje hasło wklej ten link do swojej przeglądarki : {}".format( link )
    html_content = message

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def forgot(request):  # Lenistwo level over 9000
    if request.method == 'POST':
        reset_mail = request.POST.get('reset_mail')

        try:  # Walidacja maila
            validate_email(reset_mail)
        except:
            return HttpResponse('Nieprawidłowy e-mail')

        try:  # Czy email istenije
            demand_user = User.objects.get(email=reset_mail)

            # Generate key
            salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:5]
            emailhash = hashlib.sha1(str(reset_mail).encode('utf-8')).hexdigest()[:25]
            buffor = '{}{}'.format(salt, emailhash)
            print('{} | len:{}'.format(buffor, len(buffor)))

            demand_user.profile.forgot_pass_key = buffor
            demand_user.profile.forgot_pass_expires = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
            demand_user.profile.save()

            sendEmail(reset_mail,buffor)

        except Exception as e:  # dummy
            print('dummy : {}'.format(e))

        msg = 'Na adres \'{}\' wysłaliśmy link umożliwiający zresetowanie hasła.'.format( reset_mail )
        return render(request, 'user/msg.html', {'msg': msg})

    elif request.method == 'GET':
        return render(request, 'user/forgot.html', {'title': 'Zapomniałem hasła'})


def id_generator(size=20):
    chars = "EAP0mfzu1qsQa2F9liwyG3ocHIJ4KeLt58rMvNO6SjRTg7dUnbpxVWXhkYZDGC"
    return ''.join(random.choice(chars) for _ in range(size))


def forgotReset(request, key):
    forgot_expired = False
    try:

        forgot_profile = Profile.objects.get(forgot_pass_key=key)

        # Tak dla pewności
        if forgot_profile.forgot_pass_key == '' or forgot_profile.forgot_pass_key == None:
            return HttpResponse('')

        if timezone.now() > forgot_profile.forgot_pass_expires:
            forgot_expired = True
            msg = "Twój link resetujący hasło wygasł. Prosimy ponownie skorzystać z opcji \"Zapomniałem hasła\""
            return render(request, 'user/msg.html', {'msg': msg})
        else:
            # Set randome password
            new_password = id_generator()

            UserFG = forgot_profile.user
            # UserFG.set_password('admin12345')
            UserFG.set_password(new_password)
            UserFG.save()

            # Reset reset key
            forgot_profile.forgot_pass_key = ''
            forgot_profile.save()

            return render(request, 'user/resetedPassword.html', {
                'new_password': new_password
            })

    except Exception as e:
        msg = 'Taki klucz resetujący już nie istnieje. Jeśli przez przypadek odświeżyłeś stronę nie martw się. Możesz wysłać link resetujący ponownie.'
        return render(request, 'user/msg.html', {'msg': msg})

@login_required(login_url='/user/profile/')
def changeEmail(request):
    if request.method == 'POST':
        new_mail = request.POST['newmail']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        try:  # Walidacja maila
            validate_email(new_mail)
        except:
            return HttpResponse('Wpisany email jest niepoprawny. <a href="./?=redo">Spróbuj ponownie</a>')

        if password1 != password2:
            return HttpResponse('Hasła nie są takie same. <a href="./?=redo">Spróbuj ponownie</a>')

        username = request.user
        password = password1
        auth = authenticate(username=username, password=password)

        if auth is not None:
            UserCE = User.objects.get(username=username)
            UserCE.email = new_mail
            UserCE.save()
            return redirect('Profile')
        else:
            msg = 'Oops! Hasło które wpisałeś nie jest poprawne dla twojego konta. Z przyczyn bezpieczeństwa wylogowaliśmy cię.'
            msg += 'Jeśli jesteś właścicielem konta i pomyliłeś się przy wpisywaniu zaloguj się i spróbuj ponownie.'
            logout(request)
            return render(request, 'user/msg.html', {'msg': msg})

    else:
        return render(request,'user/ChangeEmail.html')

@login_required(login_url='/user/profile/')
def changePassword(request):
    datas = {}
    datas['title'] = 'Zmień hasło'
    if request.method == 'POST':

        newpassword1 = request.POST['newpassword1']
        newpassword2 = request.POST['newpassword2']

        oldpassword1 = request.POST['oldpassword1']
        oldpassword2 = request.POST['oldpassword2']

        print( 'Nowe : {} {}'.format( newpassword1,newpassword2 ) )
        print( 'Stare : {} {}'.format( oldpassword1,oldpassword2 ) )

        if newpassword1 != newpassword2:
            return HttpResponse('Wprowadziłeś dwa różne hasła w polach <b>nowego</b> hasła <a href="./?=redo">Spróbuj ponownie</a>')

        if oldpassword1 != oldpassword2:
            return HttpResponse('Wprowadziłeś dwa różne hasła w polach <b>starego</b> hasła <a href="./?=redo">Spróbuj ponownie</a>')

        if newpassword1 == oldpassword1:
            return HttpResponse('Twoje nowe hasło nie może być takie samo jak stare hasło. <a href="./?=redo">Spróbuj ponownie</a>')

        try:
            validate_password(newpassword1)
        except Exception as e:
            msg = 'Twoje hasło nie spełnia wymagań:<br />'
            for x in e:

                if 'too short' in x:
                    msg += '&emsp;- Twoje hasło musi zawierać co najmniej 8 znaków.<br />'
                elif 'entirely numeric' in x:
                    msg += '&emsp;- Twoje hasło nie może składać się z samych cyfr.<br />'
                elif 'too similar' in x:
                    msg += '&emsp;- Twoje hasło jest zbyt podobne do loginu.<br />'
                elif 'too common' in x:
                    msg += '&emsp;- Twoje hasło jest zbyt powszechne.<br />'
                else:
                    msg += '&emsp;- {}<br />'.format( x )

            msg += '<br /><a href="./?=redo">Spróbuj ponownie</a>'
            return HttpResponse(msg)

        username = request.user
        auth = authenticate(username=username, password=oldpassword1)

        if auth is not None:
            print('logged')
            UserCP = User.objects.get(username=request.user)
            UserCP.set_password(newpassword1)
            UserCP.save()
            msg = 'Hasło zostało pomyślnie zmienione. Zaloguj się teraz na swoje konto.'
            return render(request, 'user/msg.html', {'msg': msg})
        else:
            print('oops')
            msg = 'Oops! Hasło które wpisałeś nie jest poprawne dla twojego konta. Z przyczyn bezpieczeństwa wylogowaliśmy cię.'
            msg += 'Jeśli jesteś właścicielem konta i pomyliłeś się przy wpisywaniu zaloguj się i spróbuj ponownie.'
            logout(request)
            return render(request, 'user/msg.html', {'msg': msg})

    else:
        return render(request,'user/ChangePassword.html',datas)

def profileSettingsPyCity(request):
    idict = nav(request)
    title = 'Ustawienia konta'
    return render(request,'user/settings.html',{"idict":idict,'title':title})
