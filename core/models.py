from django.db import models
from itertools import chain
from django.conf import settings 
User = settings.AUTH_USER_MODEL

# Create your models here.


CROP_GROUP_CHOICES = (
			(1, 'Texnik'),
			(2, 'Boshoqli'), 
			(3, 'Dukkaklik')
		)

class CropChoice(models.Model):
	name = models.CharField(max_length=100)
	crop_group = models.PositiveSmallIntegerField(choices=CROP_GROUP_CHOICES)

	def __str__(self):
		return f'{self.name}'

class Task(models.Model):
	title = models.CharField(max_length=50)
	description = models.TextField(null=True, blank=True)
	start_date = models.DateField(null=True)
	end_date = models.DateField(null=True)	
	crop_choice = models.ForeignKey(CropChoice, on_delete=models.RESTRICT, null=True)

	def __str__(self):
		return f'{self.title} || {self.crop_choice.name}'


class Crop(models.Model):
	crop_choice = models.ForeignKey(CropChoice, on_delete=models.RESTRICT, null=True)
	contour = models.ForeignKey('locations.Contour', on_delete=models.RESTRICT)
	description = models.TextField(null=True, blank=True)
	size = models.DecimalField(max_digits=20, decimal_places=2) # in Hectar; on what size the crop was planted
	seed = models.CharField(max_length=30)
	harvest_size = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True) # in tons; 
	year = models.IntegerField(null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	taskprogresses = models.ManyToManyField(Task, through='TaskProgress')

	def __str__(self):
		return f'{self.crop_choice.name} || {self.year} || {self.contour}'


class TaskProgress(models.Model):
	task = models.ForeignKey(Task, on_delete=models.CASCADE)
	crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	date =  models.DateField()
	size = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	
	class Meta:
		unique_together = [['task', 'crop', 'date']]

	def __str__(self):
		return f'{self.date} || {self.task.title} || {self.crop} || {self.size}'
