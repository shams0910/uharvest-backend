from django.db import transaction
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Account, LocalSupervisor, Farmer


'''
account serializer
'''

class ChangePasswordSerializer(serializers.Serializer):
	old_password = serializers.CharField(required=True)
	new_password = serializers.CharField(required=True)

	def validate_password(self, value):
		validate_password(value)
		return value




'''
editor serializers
'''

class EditorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Account
		fields = ['id', 'first_name', 'last_name', 'username', 'phone', 'role', 'region']	




'''
supervisor serializers
'''

class SupervisorSerializer(serializers.ModelSerializer):
	class Meta:
		model = LocalSupervisor
		fields = ['town', 'contours_from', 'contours_to']


class SupervisorGetSerializer(serializers.ModelSerializer):
	localsupervisor = SupervisorSerializer()

	class Meta:
		model = Account
		fields = ['id', 'username', 'first_name', 'last_name', 'phone', 'region', 'role', 'localsupervisor']




'''
observer serializers
'''

class ObserverCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Account
		fields = ['username', 'id', 'first_name', 'last_name', 'phone', 'role']
		extra_kwargs = {'password': {'required': False}}

	@transaction.atomic
	def create(self, validated_data):
		data = self.context['request'].data
		password = Account.objects.make_random_password()
		user = Account.objects.create_user(**validated_data, password=password)
		role = data['role']
		if role == 4:
			user.district_set.add(*data['districts'])
		elif role == 5:
			user.town_set.add(*data['towns'])
		return user


class DistrictObserverSerializer(serializers.ModelSerializer):
	district_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
	class Meta:
		model = Account
		fields = ['username', 'id', 'first_name', 'last_name', 'phone', 'role', 'region', 'district_set']


class TownObserverSerializer(serializers.ModelSerializer):
	town_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
	class Meta:
		model = Account
		fields = ['username', 'id', 'first_name', 'last_name', 'phone', 'role', 'region', 'town_set']




'''
farmer serializers
'''

class FarmerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Farmer
		fields = ['district']


class FarmerGetSerializer(serializers.ModelSerializer):
	farmer = FarmerSerializer()

	class Meta:
		model = Account
		fields = ['id', 'username', 'first_name', 'last_name', 'phone', 'role', 'farmer']