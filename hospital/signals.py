# hospital/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.apps import apps
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_profile_on_user_create(sender, instance, created, **kwargs):
    """
    If you have a Profile model (hospital.Profile) this will create one
    when a new User is created. If Profile doesn't exist, this is a no-op.
    """
    if not created:
        return

    try:
        Profile = apps.get_model('hospital', 'Profile')
    except LookupError:
        # Profile model not found — nothing to do (safe)
        logger.debug("Profile model not found; skipping profile creation.")
        return

    # create profile only if it doesn't already exist
    Profile.objects.get_or_create(user=instance)


@receiver(post_save)
def generic_post_save(sender, instance, created, **kwargs):
    """
    A safe generic post_save handler you can adapt.
    Example: when a Doctor model is created (hospital.Doctor) we log it.
    This handler is intentionally defensive (doesn't assume models exist).
    """
    model_name = getattr(sender, "__name__", None)
    if model_name != "Doctor":
        return  # ignore other models

    # only on creation
    if not created:
        return

    try:
        # optional: you can perform actions here, e.g., create related objects
        logger.info(f"Doctor created: {instance} (id={getattr(instance, 'id', 'n/a')})")
        # Example safe operation:
        # DoctorProfile = apps.get_model('hospital', 'DoctorProfile')
        # if DoctorProfile:
        #     DoctorProfile.objects.create(doctor=instance)
    except Exception as e:
        logger.exception("Error in generic_post_save for Doctor")
