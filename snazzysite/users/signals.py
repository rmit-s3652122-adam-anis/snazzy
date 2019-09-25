from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Address

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    When a user is saved, send signal to receiver which is this function.
    Then, this function will receive argument values from post_save:-
    instance: instance of User object
    created: check if the User is created
    """
    if created:
        Profile.objects.create(user=instance)
        # address_s = Address.objects.create(profile=profile, address_type='S')
        # address_b = Address.objects.create(profile=profile, address_type='B')

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()        