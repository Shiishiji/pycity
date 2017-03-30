# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from .models import Kategoria, Poradnik, Image
from django.contrib.auth.models import User
from django.shortcuts import get_list_or_404, get_object_or_404

# Create your views here.


# wymagany do poprawnego działania side baru
def nav(request):
    if request.user.is_authenticated():
        try:
            avatar = '/media{}'.format(request.user.profile.avatar.url.split('media')[-1])
        except:
            avatar = '/media/default.png'

        idict = {
            'is_logged': True,
            'user': request.user,
            'avatar': avatar
        }
        return idict
    else:
        idict = {
            'is_logged': False
        }
        return idict


def home(request):
    idict = nav(request)
    return render(request, 'tutorials/home.html', {
        'idict': idict,
        'title': 'PyCity - Naucz się pythona!'
    })


def kategorie(request):
    idict = nav(request)
    kats = Kategoria.objects.all()
    return render(request, 'tutorials/kategorie.html', {
        'kategorie': kats,
        'idict': idict
    })


def show_tuts(request, kat_id):
    idict = nav(request)
    tuts = get_list_or_404(Poradnik, kategoria=kat_id)
    return render(request, 'tutorials/poradniki.html', {
        'idict': idict,
        'tuts': tuts
    })


def show_tut(request, tut_id):
    idict = nav(request)
    tuts = get_list_or_404(Poradnik, pk=tut_id)
    imgs = Image.objects.filter(poradnik=tut_id)
    return render(request, 'tutorials/poradnik.html', {
        'idict': idict,
        'tut': tuts,
        'img': imgs,
    })


def img(request, img_id):
    img = get_object_or_404(Image, pk=img_id)
    return render(request, 'tutorials/img.html', {
        'img': img
    })
