from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser


def upload_location(instance, filename):
    return '{}/{}'.format(instance.id, filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(null=True, blank=True, width_field='width_field', height_field='height_field',
                               default='empty-avatar.png', upload_to=upload_location)
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)
    is_administrator = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    description = models.CharField(max_length=100, blank=True)

    def get_role_user(self):
        if self.is_administrator:
            return 'Administrator'
        if self.is_moderator:
            return 'Moderator'
        return 'User'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

