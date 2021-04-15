from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager 
from django.utils.translation import ugettext_lazy as _


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

# Create your model managers here

class CustomUserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, phone, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not phone:
            raise ValueError('The given phone must be set')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)



# Create your models here.

class Account(AbstractUser):
    username = None
    passport_number = models.CharField(max_length=10, unique=True, null=True)
    phone = models.CharField(max_length=30, null=True, unique=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
    region = models.PositiveSmallIntegerField(choices=REGION_CHOICES, default=8)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()




class Farmer(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
    district = models.ForeignKey('locations.District', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f'{self.user.phone} - {self.user.last_name}'

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




