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
	path('tasks-of-cropchoice/<int:cropchoice_id>/in-town/<int:town_id>/in-date/<str:date>/', views.TasksOfCropChoiceInTownInDate.as_view()),
	path('tasks-of-cropchoice/<int:cropchoice_id>/in-district/<int:district_id>/in-date/<str:date>/', views.TasksOfCropChoiceInDistrictInDate.as_view()),


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
]

