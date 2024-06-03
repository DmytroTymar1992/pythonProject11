from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Resume

@receiver(post_save, sender=Resume)
def save_desired_positions(sender, instance, created, **kwargs):
    if created:
        desired_positions = instance.desired_positions
        instance.desired_positions.set(desired_positions)