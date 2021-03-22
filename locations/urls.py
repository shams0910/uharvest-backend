from django.urls import path
from locations import views

urlpatterns = [
	# region views
	path('locations-in-region/<int:pk>/', views.LocationsInRegions.as_view()),
	
	# district urls here
	path('create-district/', views.CreateDistrict.as_view()),
	path('update-district/<int:pk>/', views.UpdateDistrict.as_view()),
	path('delete-district/<int:pk>/', views.DeleteDistrict.as_view()),
	
	# town urls here
	path('create-town/', views.CreateTown.as_view()),
	path('update-town/<int:pk>/', views.UpdateTown.as_view()),
	path('delete-town/<int:pk>/', views.DeleteTown.as_view()),

	# contour urls here
	path('create-contour/', views.CreateContour.as_view()),
	path('update-contour/<int:pk>/', views.UpdateContour.as_view()),
	path('delete-contour/<int:pk>/', views.DeleteContour.as_view()),
	path('contours-of-supervisor/<int:supervisor_id>/', views.ContoursOfSupervisor().as_view()),
	
]