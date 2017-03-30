from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import os


def upload_location(instance, filename):

    filename = 'avatar.{}'.format(filename.split('.')[-1])

    profile_path_dir = '{}/{}'.format(settings.MEDIA_ROOT, instance.user.username)
    profile_path_img = '{}/{}/{}'.format(settings.MEDIA_ROOT, instance.user.username, filename)

    try:
        os.mkdir(profile_path_dir)
    except:
        pass  # Folder profilu już istnieje

    return profile_path_img


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    banned = models.BooleanField(default=False)

    activation_key = models.CharField(max_length=40, null=True)
    key_expires = models.DateTimeField(null=True)

    avatar = models.ImageField( upload_to=upload_location,
                                null=True,
                                blank=True,
                                height_field='height_field',
                                width_field='width_field'
                                )
    height_field = models.IntegerField(default=0, null=True)
    width_field = models.IntegerField(default=0, null=True)

    # Zapomniałem hasła
    forgot_pass_key = models.CharField(max_length=40, null=True)
    forgot_pass_expires = models.DateTimeField(null=True)

    def __str__(self):
        return self.user.username

    def staff(self):
        return self.user.is_staff
    staff.boolean = True # Wyświetla ikonki w panelu admin zamiast True/False

    def isactive(self):
        return self.user.is_active
    isactive.boolean = True # Wyświetla ikonki w panelu admin zamiast True/False


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
