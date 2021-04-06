import datetime

#django
from django.db.models import Sum, Count, Q

#rest freamewoork
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from rest_framework.generics import (
	CreateAPIView,
	UpdateAPIView,
	DestroyAPIView,
	ListAPIView
)

#models
from .models import CropChoice, Crop, Task, TaskProgress
from locations.models import Town, District

#serializers
from .serializers import (
	CropChoiceSerializer,
	CropSerializer,
	TaskSerializer,
	TaskProgressSerializer,
	TaskProgressWithContourSerializer
)

# resources

def to_dict_from_raw(queryset):
	data = []
	for instance in queryset:
		item = instance.__dict__
		item.pop('_state')
		data.append(item)
	return data


def cotton_year_in_date(date=datetime.date.today()):
	year = date.year
	month = date.month
	if month >= 11: 
		year +=1
	return year


def to_system_date(date):
	month = date.month
	if month >= 11: 
		date = date.replace(year=2020)
	else: 
		date = date.replace(year=2021)
	return date 

	

'''
CROP CHOICE VIEWS HERE
'''

class CropChoicesWithCropGroups(APIView):
	def get(self, request):
		crop_choices = CropChoice.objects.all().values()

		crop_groups = CropChoice._meta.get_field('crop_group').choices
		crop_groups = list({'id':value, 'name': text} for value, text in crop_groups)

		return Response({'crop_choices': crop_choices, 'crop_groups':crop_groups})


class CropChoicesWithTasks(APIView):
	def get(self, request, region):
		today = datetime.date.today()
		systemdate = to_system_date(today)
		year = cotton_year_in_date()

		tasks = Task.objects.raw(
					'''
					SELECT task.*, coalesce(sum(tp.size), 0) as completed_size
					from core_task as task 
					left join core_taskprogress as tp on tp.task_id=task.id
					left join core_crop as crop on crop.id=tp.crop_id and crop.year=%s
					where %s between task.start_date and task.end_date
					group by task.id
					''', [year, systemdate]
			)
		tasks = to_dict_from_raw(tasks)


		last_7_days = tuple( (today - datetime.timedelta(days=n)).strftime('%Y-%m-%d') for n in range(0,7) )

		tp_of_last_7_days = TaskProgress.objects.raw(
								'''
								SELECT tp.date, sum(tp.size), tp.task_id as id
								from core_taskprogress as tp
								join core_crop as crop on tp.crop_id = crop.id 
								where crop.year=2021 and tp.date in %s
								group by tp.date, tp.task_id
								''', [last_7_days]
							)
		tp_of_last_7_days_serialized = to_dict_from_raw(tp_of_last_7_days)

		for task in tasks:
			tp_of_current_task = [tp for tp in tp_of_last_7_days_serialized if tp['id'] == task['id']]
			existing_dates = [tp['date'].strftime('%Y-%m-%d') for tp in tp_of_current_task]
			
			for date in last_7_days:
				if date in existing_dates: pass
				else: tp_of_current_task.append({'id': None, "date": date, 'sum':0}) 
			
			task['tp_of_last_7_days'] = tp_of_current_task

		cropchoices = CropChoice.objects\
			.filter(crop__year=2021)\
			.annotate(total_size = Sum('crop__size')).values()
		
		for cropchoice in cropchoices:
			tasks_of_current_cropchoice = [t for t in tasks if t['crop_choice_id'] == cropchoice['id']]
			cropchoice['tasks'] = tasks_of_current_cropchoice

		return Response(cropchoices)




'''
TASK VIEWS HERE
'''
class TasksOfCropChoiceInYear(APIView):
	def get(self, request, cropchoice_id, year):
		tasks = Task.objects.raw(
			'SELECT task.*, sum(tp.size) as completed_size, crop_choices.sum as total_size, min(crop_choices.year) as year\
				from core_task as task\
				left join core_taskprogress as tp on tp.task_id=task.id\
				left join core_crop as crop on crop.id=tp.crop_id\
				left join locations_contour as contour on contour.id=crop.contour_id\
				left join (\
					select sum(crop.size), crop.crop_choice_id, min(crop.year) as year\
					from core_crop as crop\
					left join locations_contour as contour on crop.contour_id=contour.id\
					where contour.supervisor_id=%s and crop.crop_choice_id=%s and crop.year=%s\
					group by crop_choice_id\
				) as crop_choices on crop_choices.crop_choice_id=task.crop_choice_id\
				where (contour.supervisor_id=%s or contour.supervisor_id is null) \
				and task.crop_choice_id=%s and (crop.year=%s or crop.year is null)\
				group by task.id, crop_choices.sum', [request.user.id, cropchoice_id, year, request.user.id, cropchoice_id, year])
		serialized_tasks = to_dict_from_raw(tasks)
		year_set = set(task['year'] for task in serialized_tasks)

		if None in year_set and len(year_set) == 1:
			return Response({'details': 'you dont have crops in this year, please add them and go back'}, status.HTTP_204_NO_CONTENT)

		return Response(serialized_tasks)


class TasksOfCropChoiceInTown(APIView):
	def get(self, request, cropchoice_id, town_id):
		year = cotton_year_in_date()

		town = Town.objects\
					.filter(id=town_id, contour__crop__year=year)\
					.annotate(total_size=Sum('contour__crop__size'))\
					.values()

		if len(town) == 0: 
			return Response({'details': f'no crops in year {year}'}, status.HTTP_204_NO_CONTENT)
		else: town = town[0]

		tasks = Task.objects\
				.filter(
					crop_choice_id=cropchoice_id, 
					taskprogress__crop__year=year,
					taskprogress__crop__contour__town_id=town_id
				)\
				.annotate(completed_size=Sum('taskprogress__size'))\
				.values()
 	
		town['tasks'] = tasks
		return Response(town)


class TasksOfCropChoiceInTownInDate(APIView):
	def get(self, request, town_id, date, cropchoice_id):
		try:
			date = datetime.datetime.strptime(date, '%Y-%m-%d').date()		
		except:
			return Response({'details': 'Not valid date'}, status.HTTP_400_BAD_REQUEST)

		year = cotton_year_in_date(date)

		town = Town.objects\
					.filter(id=town_id, contour__crop__year=year)\
					.annotate(total_size=Sum('contour__crop__size'))\
					.values()
		
		if len(town) == 0: 
			return Response({'details': f'no crops in year {year}'}, status.HTTP_204_NO_CONTENT)
		else: town = town[0]

		tasks = Task.objects\
					.filter(
						crop_choice_id=cropchoice_id, 
						taskprogress__crop__year=year,
						taskprogress__crop__contour__town_id=town_id,
						taskprogress__date__lte=date
					)\
					.annotate(completed_size=Sum('taskprogress__size'))\
					.values()

		town['tasks'] = tasks
		return Response(town) 


class TasksOfCropChoiceInDistrictInDate(APIView):
	def get(self, request, cropchoice_id, district_id, date):
		try:
			date = datetime.datetime.strptime(date, '%Y-%m-%d').date()		
		except:
			return Response({'details': 'Not valid date'}, status.HTTP_400_BAD_REQUEST)
		
		year = cotton_year_in_date(date)

		district = District.objects\
						.filter(
							id=district_id, 
							town__contour__crop__year=year, 
							town__contour__crop__crop_choice_id=cropchoice_id
						)\
						.annotate(total_size=Sum('town__contour__crop__size'))\
						.values()
		
		if len(district) == 0: 
			return Response({'details': f'no crops in year {year}'}, status.HTTP_204_NO_CONTENT)
		else: district = district[0]
		
		tasks = Task.objects\
					.filter(
						crop_choice_id=cropchoice_id, 
						taskprogress__crop__year=year,
						taskprogress__crop__contour__town__district_id=district_id,
						taskprogress__date__lte=date
						)\
					.annotate(completed_size=Sum('taskprogress__size'))\
					.values()
		
		district['tasks'] = tasks
		
		return Response(district)



'''
CROP VIEWS HERE
'''

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




'''
TASKPROGRESS VIEWS HERE
'''

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


