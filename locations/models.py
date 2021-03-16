from django.db import models
from django.conf import settings 

User = settings.AUTH_USER_MODEL 
# Create your models here.


REGION_CHOICES = (
		(8, "Qashqadaryo"),
		(2, "Andijan")
	)

class District(models.Model):
	name = models.CharField(max_length=40)
	region = models.PositiveSmallIntegerField(choices=REGION_CHOICES) 
	officer = models.ManyToManyField(User, blank=True, limit_choices_to={'role':4})

	def __str__(self):
		return f'{self.name}:{self.id}, {self.get_region_display()}:{self.region}'
	
	def get_region(self):
		return f'{self.region}:{self.get_region_display()}'

		
class Town(models.Model):
	name = models.CharField(max_length=40)
	district = models.ForeignKey(District, on_delete=models.RESTRICT)
	officer = models.ManyToManyField(User, blank=True, limit_choices_to={'role':5})

	def __str__(self):
		return f'{self.name}:{self.id}, {self.district}'

class Contour(models.Model):
	number = models.CharField(max_length=10)
	region = models.PositiveSmallIntegerField(choices=REGION_CHOICES)
	town = models.ForeignKey(Town, on_delete=models.RESTRICT)
	supervisor = models.ForeignKey('accounts.LocalSupervisor', on_delete=models.RESTRICT, related_name='supervising_contours', null=True)
	farmer = models.ForeignKey('accounts.Farmer', on_delete=models.RESTRICT, null=True)
	size = models.DecimalField(max_digits=22, decimal_places=2, null=True)
	
	def __str__(self):
		return f'{self.number} || {self.town.name} || S - {self.supervisor_id}'