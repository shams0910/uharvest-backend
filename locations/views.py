#django
from django.db import transaction
from django.core.cache import cache
from django.db.models import Count

#rest framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from .models import District, Town, Contour

from rest_framework.generics import (
	CreateAPIView,
	UpdateAPIView,
	DestroyAPIView
)

#models
from accounts.models import (
	LocalSupervisor, 
	Farmer, 
	Account as User
)

#serializers
from .serializers import ( 
	DistrictSerializer, 
	TownSerializer, 
	ContourSerializer,
	ContourWithFarmerSerializer
)



# region views here
class LocationsInRegions(APIView):
	@transaction.atomic
	def get(self, request, pk):
		data = cache.get('locations')
		if data:
			return Response(data)

		towns = Town.objects.filter(district__region=pk).values()
		districts = District.objects\
						.filter(region=pk)\
						.annotate(
							farmers=Count('farmer', distinct=True), 
							contours=Count('town__contour', distinct=True)
						)
		cache.set('locations', {'districts': districts.values(), 'towns': towns}, 7200)

		return Response({'districts': districts.values(), 'towns': towns})


# district views here
class CreateDistrict(CreateAPIView):
	queryset = District.objects.all()
	serializer_class = DistrictSerializer

class UpdateDistrict(UpdateAPIView):
	queryset = District.objects.all()
	serializer_class = DistrictSerializer

class DeleteDistrict(DestroyAPIView):
	queryset = District.objects.all()
	serializer_class = DistrictSerializer


# town views here
class CreateTown(CreateAPIView):
	queryset = Town.objects.all()
	serializer_class = TownSerializer

class UpdateTown(UpdateAPIView):
	queryset = Town.objects.all()
	serializer_class = TownSerializer

class DeleteTown(DestroyAPIView):
	queryset = Town.objects.all()
	serializer_class = TownSerializer


# contour views here
class CreateContour(CreateAPIView):
	queryset = Contour.objects.all()
	serializer_class = ContourSerializer

class UpdateContour(UpdateAPIView):
	queryset = Contour.objects.all()
	serializer_class = ContourSerializer

class DeleteContour(DestroyAPIView):
	queryset = Contour.objects.all()
	serializer_class = ContourSerializer

class ContoursOfSupervisor(APIView):
	def get(self, request, supervisor_id):
		contours = Contour.objects.select_related('farmer__user').filter(supervisor_id=supervisor_id)
		serialized_contours = ContourWithFarmerSerializer(contours, many=True).data
		return Response(serialized_contours)

class ContoursOfFarmer(APIView):
	def get(self, request, farmer_id):
		contours = Contour.objects.filter(farmer_id=farmer_id).values()
		return Response(contours)