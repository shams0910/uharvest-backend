from django.db import transaction
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from .models import District, Town, Contour

from rest_framework.generics import (
	CreateAPIView,
	UpdateAPIView,
	DestroyAPIView
)

from accounts.models import (
	LocalSupervisor, 
	Farmer, 
	Account as User
)

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
		towns = Town.objects.filter(district__region=pk).values()
		districts = District.objects.filter(region=pk)\
		.annotate(farmers=Count('farmer'), contours=Count('town'))\
		.values()
		return Response({'districts': districts, 'towns': towns}, status.HTTP_200_OK)


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

class DistrictList(APIView):
	def get(self, request, region_id):
		districts = District.objects\
			.filter(region=region_id)\
			.annotate(farmers=Count('farmer'), contours=Count('contour'))
		return Response(districts.values())


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

class TownList(APIView):
	def get(self, request, district_id):
		towns = Town.objects.filter(district_id=district_id)
		return Response(towns.values())


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