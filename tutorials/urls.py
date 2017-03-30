"""tutorials URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from . import views
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.views.generic.base import RedirectView


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^poradniki$', views.kategorie, name='kats'),
    url(r'^poradniki/(?P<kat_id>[0-9]+)/$', views.show_tuts, name='tuts'),
    url(r'^poradniki/(\d)/(?P<tut_id>[0-9]+)$', views.show_tut, name='tut'),
    url(r'^img/(?P<img_id>[0-9]+)$', views.img, name='img'),
    #url(r'^666$', RedirectView.as_view(url=reverse('admin:index')), name='admin'),
]
