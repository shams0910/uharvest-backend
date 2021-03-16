from rest_framework.serializers import (
	ModelSerializer, Serializer,
	StringRelatedField, CharField, IntegerField)
from .models import District, Town, Contour
from accounts.models import Farmer


class DistrictSerializer(ModelSerializer):
	class Meta:
		model = District
		fields = ['id', 'name', 'region']
		read_only_fields = ('id',)


class DistrictGetSerializer(ModelSerializer):
	region_display = StringRelatedField(source='get_region')
	class Meta:
		model = District
		fields = ['id', 'name', 'region_display']
		read_only_fields = ('id',)


class TownSerializer(ModelSerializer):
	class Meta:
		model = Town
		fields = ['id', 'name', 'district']
		read_only_fields = ('id',)

 
class ContourSerializer(ModelSerializer):
	class Meta:
		model = Contour
		fields = '__all__'
		read_only_fields = ('id',)


class FarmerSerializer(ModelSerializer):
	first_name = CharField(source='user.first_name')
	last_name = CharField(source='user.last_name')
	id = IntegerField(source='user_id')
	class Meta:
		model = Farmer
		fields = ['id', 'first_name', 'last_name']
		read_only_fields = ('id',)


class ContourWithFarmerSerializer(ModelSerializer):
	farmer = FarmerSerializer()
	class Meta:
		model = Contour
		fields = ['id', 'number', 'town', 'supervisor_id', 'size', 'farmer']