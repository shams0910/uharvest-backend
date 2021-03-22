from rest_framework.serializers import Serializer, ModelSerializer, CharField, IntegerField
from .models import CropChoice, Crop, Task, TaskProgress
from accounts.models import Farmer




# cropchoice seriliazers 
class CropChoiceSerializer(ModelSerializer):
	class Meta:
		model = CropChoice
		fields = '__all__'


# crop seriliazers 
class CropSerializer(ModelSerializer):
	crop_choice = CharField(source='crop_choice.name', required=False)
	class Meta:
		model = Crop
		fields = [ "id", "crop_choice_id", "contour_id", "description", "size", "seed", "harvest_size", "year", "crop_choice"]
		read_only_fields = ('id', 'created_at', 'updated_at')



# task seriliazers 
class TaskSerializer(ModelSerializer):
	class Meta:
		model = Task
		fields = "__all__"
		read_only_fields = ('id', 'created_at', 'updated_at')


# taskprogress seriliazers 
class TaskProgressSerializer(ModelSerializer):
	class Meta:
		model = TaskProgress
		fields = "__all__"
		read_only_fields = ('id', 'created_at', 'updated_at')
		extra_kwargs = {'task': {'required': False}, 'crop': {'required': False}, 'date': {'required': False},}


class FarmerSerializer(Serializer):
	id = IntegerField(source='user_id')
	last_name = CharField(source='user.last_name')
	first_name = CharField(source='user.first_name')
	phone = CharField(source='user.phone')


class TaskProgressWithContourSerializer(ModelSerializer):
	contour_number = IntegerField(source='crop.contour.number')
	farmer = FarmerSerializer(source='crop.contour.farmer')

	class Meta:
		model = TaskProgress
		fields = ['id', 'task_id', 'crop_id', 'date', 'size', 'contour_number', 'farmer']
		read_only_fields = ('id', 'created_at', 'updated_at')