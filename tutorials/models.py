from django.db import models
from user.models import Profile

# Tutorials/models.py
# Create your models here.


class Kategoria(models.Model):
    nazwa = models.CharField(max_length=40)
    opis = models.TextField(default="-- Brak opisu --")

    def __str__(self):
        return self.nazwa


class Poradnik(models.Model):
    kategoria = models.ForeignKey(Kategoria, default=0)
    tytul = models.CharField(max_length=150)
    tresc = models.TextField()
    opis = models.CharField(max_length=150, default="")

    PYTHON2 = "P2"
    PYTHON3 = "P3"
    PYTHON = "PP"

    VERSIONS = (
        (PYTHON2, 'Python 2.7'),
        (PYTHON3, 'Python 3.5'),
        (PYTHON, 'Python 2.7 and 3.5'),
    )

    version = models.CharField(
        max_length=2,
        choices=VERSIONS,
        default=PYTHON,
    )

    def __str__(self):
        return '{} | {}'.format(self.kategoria.nazwa, self.tytul)


class Image(models.Model):
    poradnik = models.ForeignKey(Poradnik)
    nazwa = models.CharField(max_length=40, default="", blank=True)

    def upload_location(self, filename):
        url = 'tuts/{}/{}'.format(str(self.poradnik.pk), str(filename))
        return url

    image = models.ImageField(
        upload_to=upload_location
    )

    def __str__(self):
        return 'Kategoria: {} Tutorial:{}. {} Image: {}'.format(
            self.poradnik.kategoria.nazwa, self.poradnik.pk,
            self.poradnik.tytul, self.nazwa)


class File(models.Model):
    poradnik = models.ForeignKey(Poradnik, blank=True)
    nazwa = models.CharField(max_length=40, default="", blank=True)

    def upload_location(self, filename):
        if self.poradnik.pk:
            url = 'files/{}/{}'.format(str(self.poradnik.pk), str(filename))
        else:
            url = 'files/{}/{}'.format(str(filename))
        return url