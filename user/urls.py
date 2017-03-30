from django.conf.urls import url
from . import views

urlpatterns = [

    # Strona logowania
    url(r'^login/$', views.Login.as_view(), name="Login"),

    # Rejestracja
    url(r'^registration/$', views.register, name="Registration"),

    # Profil użytkownika
    url(r'^profile/', views.profile, name="Profile"),

    # Aktywacja konta użytkownika
    url(r'^activate/(?P<key>.+)$', views.activation),

    # Podziękowanie za rejestrację
    url(r'^thanks$', views.thanks_for_reg, name="thanks"),

    # Wylogowanie
    url(r'^logout$', views.logoutUser, name="Logout"),

    # Ponowne wysłanie linka aktywującego
    url(r'^resend-activation-mail/(?P<user_id>[0-9]+)/$', views.new_activation_link),

    # Zapomniałem hasła
    url(r'^forgot$', views.forgot, name="Forgot"),

    # Resetuj hasło
    url(r'^passreset/(?P<key>.+)/$', views.forgotReset, name="ForgotReset"),

    # Zmień email
    url(r'^emailchange/$',views.changeEmail,name="EmailChange"),

    # Zmień hasło
    url(r'^passchange/$',views.changePassword,name="PasswordChange"),

    # Ustawienia - PyCity - Poradniki
    url(r'^settings/$',views.profileSettingsPyCity,name="PyCitySettings"),
]
