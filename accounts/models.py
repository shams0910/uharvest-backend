from django.db import models, IntegrityError
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver


REGION_CHOICES = (
    (8, "Qashqadaryo"),
    (2, "Andijan")
)

ROLE_CHOICES = (
      # (1, 'president'),
    (2, 'governor'),
    (3, 'editor'),
    (4, 'district_officer'),
    (5, "town_officer"),
    (6, 'supervisor_or_farmer')
)

# Create your models here.

class Account(AbstractUser):
  	phone = models.CharField(max_length=30, null=True)
  	role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
  	region = models.PositiveSmallIntegerField(choices=REGION_CHOICES, default=8)


class Farmer(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
    district = models.ForeignKey('locations.District', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.user.last_name}'

class LocalSupervisor(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
    town = models.ForeignKey('locations.Town', on_delete=models.SET_NULL, null=True)
    contours_from = models.PositiveSmallIntegerField(null=True)
    contours_to = models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        return f'{self.user.last_name}:{self.user_id} {self.town}'
 

class Editor(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
    region = models.PositiveSmallIntegerField(choices=REGION_CHOICES)




