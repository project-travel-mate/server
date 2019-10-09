from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from api.modules.users.enums import PasswordVerificationModeChoice


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.TextField(validators=[URLValidator()], default=None, null=True)
    status = models.TextField(null=True, default=None)
    last_active = models.DateTimeField(null=True)
    is_verified = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        # for users already created
        Profile.objects.create(user=instance)


class PasswordVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    mode = models.TextField(max_length=30,
                            default=PasswordVerificationModeChoice.FORGET_PASSWORD,
                            choices=[(tag, tag.value) for tag in PasswordVerificationModeChoice])
    created = models.DateTimeField(auto_now=True)
