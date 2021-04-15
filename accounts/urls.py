from django.urls import path
from accounts import views

urlpatterns = [
	# change password and account urls here
	path('auto-login/', views.AutoLogin.as_view()),
	path('delete-user/<int:pk>/', views.DeleteUser.as_view()),
	path('change-password/', views.ChangePassword.as_view()),
	
	# supervisor urls here
	path('login-supervisor/', views.LoginSupervisor.as_view()),
	path('create-supervisor/', views.CreateSupervisor.as_view()),
	path('update-supervisor/<int:pk>/', views.UpdateSupervisor.as_view()),
	path('supervisors-in-region/<int:pk>/', views.SupervisorsInRegion.as_view()),
	# add supervisors in district and region

	# farmer urls here
	path('create-farmer/', views.CreateFarmer.as_view()),
	path('update-farmer/<int:pk>/', views.UpdateFarmer.as_view()),
	path('farmers-in-district/<int:district_id>/', views.FarmersInDistrict.as_view()),
	# add farmer contours

	# observer urls here
	path('login-observer/', views.LoginObserver.as_view()),
	path('create-observer/', views.CreateObserver.as_view()),
	# path('update-observer/<int:pk>/', views.UpdateSupervisor.as_view()),
	path('observers-in-region/<int:region_id>/', views.ObserversInRegion.as_view()),
	# most of observer related views will be in lacations app or in core app

	# editor urls here
	path('login-editor/', views.LoginEditor.as_view()),
]
