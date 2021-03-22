# django imports
from django.db import transaction, IntegrityError
from django.db.models import Q
from django.contrib.auth import authenticate

# rest framework imports
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView, CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status

# serializer imports
from .serializers import (
	EditorSerializer, SupervisorGetSerializer, FarmerGetSerializer, GovernorSerializer,
	ObserverCreateSerializer, DistrictObserverSerializer, TownObserverSerializer,
	ChangePasswordSerializer
)

# model imports
from rest_framework.authtoken.models import Token
from accounts.models import LocalSupervisor, Farmer, Account as User
from locations.models import District, Town, Contour

# Create your views here.


"""
GENERAL ACCOUNT VIEWS HERE
"""

class AutoLogin(APIView):
	@transaction.atomic
	def post(self, request):
		user = request.user
		platform = request.data.get("platform")

		if type(platform) is not list: platform = [platform]
		print(user.role, platform)
		if user.role in platform:
			token = request.auth

			if user.role == 3:
				serialized_user = EditorSerializer(user).data
			elif user.role == 6:
				serialized_user = SupervisorGetSerializer(user).data
			elif user.role == 2:
				serialized_user = SupervisorGetSerializer(user).data
			elif user.role == 4:
				serialized_user = DistrictObserverSerializer(user).data
			elif user.role == 5:
				serialized_user = TownObserverSerializer(user).data
			
			return Response({'token': token.key, 'user': serialized_user})

		return Response(status=status.HTTP_401_UNAUTHORIZED)


class ChangePassword(UpdateAPIView):
	def get_object(self, queryset=None):
		return self.request.user

	def put(self, request, *args, **kwargs):
		self.object = self.get_object()
		serializer = ChangePasswordSerializer(data=request.data)
		if serializer.is_valid():
			old_password = serializer.data.get('old_password')

			if not self.object.check_password(old_password):
				return Response({"old_password": "Wrong old password"}, status.HTTP_400_BAD_REQUEST)
			self.object.set_password(serializer.data.get("new_password"))
			self.object.save()
			return Response(status=status.HTTP_204_NO_CONTENT)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteUser(APIView):
	def delete(self, request, pk):
		try:
			user = User.objects.get(pk=pk).delete()
		except User.DoesNotExist:
			return Response('User not found', status=status.HTTP_404_NOT_FOUND)
		except User.IntegrityError:
			return Response({'details': 'The user you trying to delete has relations'})
		
		return Response('User deleted', status=status.HTTP_204_NO_CONTENT)




"""
EDITOR VIEWS HERE
"""


class LoginEditor(APIView):
	permission_classes = []
	def post(self, request):
		user = authenticate(
			username=request.data.get('username'), 
			password=request.data.get("password")
		)
		if user is not None:
			if user.is_active and user.role == 3:
				token, created = Token.objects.get_or_create(user=user)
				serialized_user = EditorSerializer(user).data
				return Response({'token': token.key, 'user': serialized_user})
			else:
				return Response({"details": 'Only editor is allowed'}, status.HTTP_403_FORBIDDEN)
		return Response({"details": 'Login or password is wrong'}, status.HTTP_401_UNAUTHORIZED)




"""
SUPERVISOR VIEWS HERE
"""

class CreateSupervisor(APIView):
	@transaction.atomic
	def post(self, request):
		town_id = request.data.pop('town_id')
		contours_from = request.data.pop('contours_from', None)
		contours_to = request.data.pop('contours_to', None)

		password = User.objects.make_random_password()
		try:
			user = User.objects.create_user(**request.data, password=password)
		except TypeError as e:
			return Response({'details': f'{e}'}, status.HTTP_400_BAD_REQUEST)
		profile = LocalSupervisor.objects.create(
			user_id=user.id, 
			town_id=town_id, 
			contours_from=contours_from, 
			contours_to=contours_to
		)
		user.localsupervisor = profile
		serialized_user = SupervisorGetSerializer(user).data
		return Response(serialized_user, status=status.HTTP_201_CREATED)


class UpdateSupervisor(APIView):
	@transaction.atomic
	def put(self, request, pk):
		try:
			supervisor = LocalSupervisor.objects.select_related('user').get(pk=pk)
		except Exception as e:
			return Response({'details' : f'{e}'}, status.HTTP_400_BAD_REQUEST)
		supervisor.user.first_name = request.data.get('first_name', supervisor.user.first_name)
		supervisor.user.last_name = request.data.get('last_name', supervisor.user.last_name)
		supervisor.user.phone = request.data.get('phone', supervisor.user.phone)
		supervisor.town_id = request.data.get('town_id', supervisor.town_id)
		supervisor.user.save()
		supervisor.save()
		serialized_user = SupervisorGetSerializer(supervisor).data

		return Response(serialized_user, status=status.HTTP_200_OK)
	
		
class SupervisorsInRegion(APIView):
	def get(self, request, pk):
		supervisors = User.objects.select_related('localsupervisor')\
			.filter(region=pk, localsupervisor__isnull=False)
		serialized_supervisors = SupervisorGetSerializer(supervisors, many=True).data
		return Response(serialized_supervisors, status.HTTP_200_OK)


class LoginSupervisor(APIView):
	permission_classes = []
	# x9shSD5fvs supervisor1
	def post(self, request):
		user = authenticate(
			username=request.data.get('username'), 
			password=request.data.get("password")
		)
		if user is not None:
			if user.is_active and user.role == 6:
				serialized_user = SupervisorGetSerializer(user).data
				token, created = Token.objects.get_or_create(user=user)
				return Response({'token': token.key, 'user' : serialized_user }, status=status.HTTP_200_OK)
		
		return Response({"details": 'Login or password is wrong'}, status.HTTP_401_UNAUTHORIZED)




"""
FARMER VIEWS HERE
"""

class CreateFarmer(APIView):
	@transaction.atomic
	def post(self, request):
		district = request.data.pop('district')
		password = User.objects.make_random_password()
		try:
			user = User.objects.create_user(**request.data, password=password)
		except IntegrityError as e:
			return Response({'details': f'{e}'}, status.HTTP_409_CONFLICT)
		# except 
		profile = Farmer.objects.get_or_create(user=user, district_id=district)
		serialized_user = FarmerGetSerializer(user).data
		return Response(serialized_user, status=status.HTTP_201_CREATED)


class FarmersInDistrict(APIView):
	def get(self, request, district_id):
		farmers_in_district = User.objects\
			.select_related('farmer')\
			.filter(farmer__district_id=district_id)
		serialized_farmers = FarmerGetSerializer(farmers_in_district, many=True).data
		return Response(serialized_farmers)




"""
OBSERVER VIEWS HERE
"""

class CreateObserver(CreateAPIView):
	queryset = User.objects.all()
	serializer_class = ObserverCreateSerializer


class UpdateObserver(APIView):
	@transaction.atomic
	def post(self, request, pk):
		try: 
			user = User.objects.get(pk=pk)
		except User.DoesNotExist as e:
			return Response({'details': f'{e}'})
		user.username = request.data.get('username', user.username)
		user.first_name = request.data.get('first_name', user.first_name)
		user.last_name = request.data.get('last_name', user.username)
		user.phone = request.data.get('phone', user.phone)

		role = request.data.get('role')
		towns = request.data.get('towns', None)
		districts = request.data.get('districts', None)
		if role == 4 and districts:
			user.district_set.clear()
			user.district_set.add(*districts)
		elif role == 5 and towns:
			user.district_set.clear()
			user.district_set.add(*towns)
		user.save()
		return Response(UserSerializer(user).data)


class ObserversInRegion(APIView):
	def get(self, request, region_id):
		observers = User.objects.filter(role__in=[4,5], region=8).values('id', 'last_name', 'first_name', 'username', 'role')
		districts_of_observers = District.officer.through.objects.filter(district__region=region_id).values('account_id', 'district_id', 'district__name')
		towns_of_observers = Town.officer.through.objects.filter(town__district__region=region_id).values('account_id', 'town_id', 'town__name')
		return Response({
			'observers': observers, 
			'districts_of_observers':districts_of_observers,
			'towns_of_observers': towns_of_observers
		})


class LoginObserver(APIView):
	permission_classes = []
	def post(self, request):
		user = authenticate(
			username=request.data.get('username'), 
			password=request.data.get("password")
		)
		if user is not None:
			if user.is_active:
				token, created = Token.objects.get_or_create(user=user)
				if user.role == 2:
					serialized_user = GovernorSerializer(user).data
				elif user.role == 4:
					serialized_user = DistrictObserverSerializer(user).data
				elif user.role == 5:
					serialized_user = TownObserverSerializer(user).data
				
				return Response({'token':token.key, 'user': serialized_user})

		return Response({"details": 'Login or password is wrong'}, status.HTTP_401_UNAUTHORIZED)





