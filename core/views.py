import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from .models import CropChoice, Crop, Task, TaskProgress

from rest_framework.generics import (
	CreateAPIView,
	UpdateAPIView,
	DestroyAPIView,
	ListAPIView
)

from .serializers import (
	CropChoiceSerializer,
	CropSerializer,
	TaskSerializer,
	TaskProgressSerializer,
	TaskProgressWithContourSerializer
)

# crop choice views here
class CropChoicesWithCropGroups(APIView):
	def get(self, request):
		crop_choices = CropChoice.objects.all().values()
		crop_groups = CropChoice._meta.get_field('crop_group').choices
		crop_groups = list({'id':value, 'name': text} for value, text in crop_groups)
		return Response({'crop_choices': crop_choices, 'crop_groups':crop_groups})


# task views here
class TasksOfCropChoice(APIView):
	def get(self, request, cropchoice_id):
		tasks = Task.objects.filter(crop_choice_id=cropchoice_id)
		serialized_tasks = TaskSerializer(tasks, many=True).data
		return Response(serialized_tasks)


# crop views here
# class CreateCrop(CreateAPIView):
# 	queryset = Crop.objects.all()
# 	serializer_class = CropSerializer

class CreateCrop(APIView):
	def post(self, request):
		try:
			crop = Crop.objects.create(**request.data)
		except ValueError as e:
			return Response({'details': f'{e}'}, status.HTTP_400_BAD_REQUEST)
		serialized_crop = CropSerializer(crop).data
		return Response(serialized_crop)


class UpdateCrop(UpdateAPIView):
	queryset = Crop.objects.all()
	serializer_class = CropSerializer

class DeleteCrop(DestroyAPIView):
	queryset = Crop.objects.all()
	serializer_class = CropSerializer

class CropsInContour(APIView):
	def get(self, request, pk):
		crops_in_contour = Crop.objects.select_related('crop_choice').filter(contour_id=pk)
		serialized_crops_in_contour = CropSerializer(crops_in_contour, many=True).data
		return Response(serialized_crops_in_contour)


# taskprogress views here
class CreateTaskProgress(CreateAPIView):
	queryset = TaskProgress.objects.all()
	serializer_class = TaskProgressSerializer

class CreateTaskProgressesInDate(APIView):
	# in the lines below, task progress referenced as tp
	def post(self, request):
		print(request.user.id)
		try:
			date = datetime.datetime.strptime(request.data.get('date'), '%Y-%m-%d').date()		
		except:
			return Response({'details': 'Not valid date'}, status.HTTP_400_BAD_REQUEST)

		task_id = request.data.get('task_id')
		cropchoice_id = request.data.get('cropchoice_id') 
		if not (task_id and cropchoice_id):
			return Response({'details': 'task_id and cropchoice_id is necessary'}, status.HTTP_400_BAD_REQUEST)

		year = request.data.get('year')
		if year and type(year) == int:
			crop_ids = Crop.objects.filter(year=year, contour__supervisor_id=request.user.id, crop_choice_id=cropchoice_id).values_list('id', flat=True)
			tps = []
			for crop_id in crop_ids:
				tp = {
					'task_id': task_id,
					'crop_id': crop_id,
					'date': date,				
				}
				tp_instance = TaskProgress(**tp)
				tps.append(tp_instance)
			TaskProgress.objects.bulk_create(tps, ignore_conflicts=True)
		else:
			return Response({'details': 'year is necessary; year should be integer'}, status.HTTP_400_BAD_REQUEST)
		
		return Response([crop_ids, request.user.id])


# class


class UpdateTaskProgress(UpdateAPIView):
	queryset = TaskProgress.objects.all()
	serializer_class = TaskProgressSerializer

class DeleteTaskProgress(DestroyAPIView):
	queryset = TaskProgress.objects.all()
	serializer_class = TaskProgressSerializer

class TaskProgressesInContour(APIView):
	def get(self, request, pk):
		task_progresses_in_contour = TaskProgress.objects.filter(crop__contour__id=pk)
		return Response(task_progresses_in_contour.values())


class TaskProgressesOfTaskByContoursInYear(APIView):
	def get(self, request, task_id, year):
		task_progresses = TaskProgress.objects.select_related('crop__contour__farmer__user').filter(task_id=task_id, crop__year=year, crop__contour__supervisor_id=request.user.id)
		serialized_task_progresses = TaskProgressWithContourSerializer(task_progresses, many=True).data
		dates = set(tp['date'] for tp in serialized_task_progresses)
		return Response({'dates': dates, 'tps': serialized_task_progresses})


class TaskProgressesByTownInDistrictInDate(APIView):
	# Get TaskProgresses(TP) by towns in district. Output will be sum of TP in HE
	def get(self, request, district_id, date):
		try:
			date = datetime.datetime.strptime(date, '%Y-%m-%d').date()		
		except:
			return Response({'details': 'Not valid date'}, status.HTTP_400_BAD_REQUEST)
		
		task_progresses = TaskProgress.objects.raw(
		'SELECT task.id AS id, task.title,  sum(tp.size), town.name \
			FROM core_taskprogress AS tp \
			LEFT JOIN core_task AS task ON tp.task_id=task.id \
			LEFT JOIN core_crop AS crop ON crop.id=tp.crop_id \
			LEFT JOIN locations_contour AS contour ON crop.contour_id=contour.id \
			LEFT JOIN locations_town AS town ON town.id=contour.town_id \
			WHERE town.district_id=%s AND tp.date=%s\
			GROUP by task.id, town.id',
			[district_id, date]
			)
		data = []
		for tp in task_progresses:
			item = tp.__dict__
			item.pop('_state')
			data.append(item)
			print(item)
		return Response(data) 
		select task.*, sum(tp.size) as completed_size, sum(crop.size) as total_size
from core_task as task
full join core_taskprogress as tp on tp.task_id=task.id
full join core_crop as crop on crop.id=tp.crop_id
where task.crop_choice_id=1 and (crop.year=2021 or crop.year is null)
group by task.id

# class ListTaskProgressesByTownInDistrictInMonth(APIView):
# 	# Get TaskProgresses(TP) by towns in district. Output will be sum of TP in HE
# 	def get(self, request, district_id, month, year):
# 		print(month)
# 		if month is None or year is None or (month>12 or month<1):
# 			return Response('Invalid parameters', status.HTTP_400_BAD_REQUEST) 
		
# 		task_progresses = TaskProgress.objects.raw(
# 		'select task.id AS id, task.title,  sum(tp.size), town.name \
# 			FROM core_taskprogress AS tp \
# 			LEFT JOIN core_task AS task ON tp.task_id=task.id \
# 			LEFT JOIN core_crop AS crop ON crop.id=tp.crop_id \
# 			LEFT JOIN locations_contour AS contour ON crop.contour_id=contour.id \
# 			LEFT JOIN locations_town AS town ON town.id=contour.town_id \
# 			WHERE town.district_id=%s AND MONTH(tp.date)=%s AND YEAR(tp.date)=%s\
# 			GROUP by task.id, town.id',
# 			[district_id, month, year]
# 			)
# 		data = []
# 		for tp in task_progresses:
# 			item = tp.__dict__
# 			item.pop('_state')
# 			data.append(item)
# 			print(item)
# 		return Response(data)

