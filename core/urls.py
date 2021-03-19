from django.urls import path
from core import views

# taskprogress related urls referenced as 'tp'

urlpatterns = [
	# cropchoice urls here
	path('cropchoices-with-cropgroups/', views.CropChoicesWithCropGroups.as_view()),
	path('cropchoices-with-tasks-in-region/<int:region>/', views.CropChoicesWithTasks.as_view()),
	# task urls here
	path('tasks-of-cropchoice/<int:cropchoice_id>/in-year/<int:year>/', views.TasksOfCropChoiceInYear.as_view()),
	path('tasks-of-cropchoice/<int:cropchoice_id>/in-town/<int:town_id>/', views.TasksOfCropChoiceInTown.as_view()),


	# crop urls here
	path('create-crop/', views.CreateCrop.as_view()),
	path('update-crop/<int:pk>/', views.UpdateCrop.as_view()),
	path('delete-crop/<int:pk>/', views.DeleteCrop.as_view()),
	path('crops-in-contour/<int:pk>/', views.CropsInContour.as_view()),

	#taskprogress urls here
	path('create-tp/', views.CreateTaskProgress.as_view()),
	path('create-tps-in-date/', views.CreateTaskProgressesInDate.as_view()),
	path('update-tp/<int:pk>/', views.UpdateTaskProgress.as_view()),
	path('delete-tp/<int:pk>/', views.DeleteTaskProgress.as_view()),
	path('tp-of-task-by-contours/<int:task_id>/in-year/<int:year>/', views.TaskProgressesOfTaskByContoursInYear.as_view()),
	path('tp-of-cropchoice/<int:cropchoice_id>/by-town-in-district/<int:district_id>/in-date/<str:date>/', views.TaskProgressesOfCropChoiceByTownInDistrictInDate.as_view()),
	path('tp-of-cropchoice/<int:cropchoice_id>/by-district-in-region/<int:region>/in-date/<str:date>/', views.TaskProgressesOfCropChoiceByDistrictInRegionInDate.as_view()),

	# path('tp-by-town-in-district/<int:district_id>/in-month/<int:month>/<int:year>/', views.ListTaskProgressesByTownInDistrictInMonth.as_view()),
]
"""
select tp.id, tp.date, tp.size, tp.crop_id, tp.task_id, crop.id, crop.size, crop.crop_choice_id, cropchoice.name
from core_taskprogress as tp
right join core_crop as crop on tp.crop_id=crop.id
left join core_cropchoice as cropchoice on cropchoice.id=crop.crop_choice_id
where crop.crop_choice_id=1
select tp.task_id, sum(tp.size) as completed_size, crop_sizes.total_size, contour.id, contour.number
from core_taskprogress as tp
right join core_crop as crop on tp.crop_id=crop.id
left join core_cropchoice as cropchoice on cropchoice.id=crop.crop_choice_id
left join locations_contour as contour on crop.contour_id=contour.id
left join (SELECT crop.size as total_size, crop.id, crop.crop_choice_id,contour.id AS contour_id, contour.number 
		   FROM core_crop as crop 
LEFT JOIN locations_contour as contour ON crop.contour_id = contour.id
WHERE crop.crop_choice_id = 1) as crop_sizes on crop_sizes.contour_id = contour.id
where crop.crop_choice_id=1
group by contour.id, tp.task_id, crop_sizes.total_size;

SELECT task.*, sum(tp.size) as completed_size, crop_choices.sum as total_size, min(crop.year) as year
from core_task as task
left join core_taskprogress as tp on tp.task_id=task.id
left join core_crop as crop on crop.id=tp.crop_id
left join locations_contour as contour on contour.id=crop.contour_id
left join (
	select sum(crop.size), crop.crop_choice_id
	from core_crop as crop
	left join locations_contour as contour on crop.contour_id=contour.id
	where crop_choice_id=1 and contour.supervisor_id=5 and crop.year=2021
	group by crop_choice_id
) as crop_choices on crop_choices.crop_choice_id=crop.crop_choice_id
where (contour.supervisor_id=5 or contour.supervisor_id is null) 
and task.crop_choice_id=1 and (crop.year=2021 or crop.year is null)
group by task.id, crop_choices.sum



"""