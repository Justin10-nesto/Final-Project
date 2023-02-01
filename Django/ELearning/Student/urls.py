
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.loginPage, name='loginPage'),
    path('searchUserSelected', views.searchUserSelected, name = "searchUserSelected"),
    path('register', views.registerPage, name ='registerPage'),
    path('submitRegistration', views.submitRegistration, name = 'submitRegistration'),
    path('userProfile', views.userProfilePage, name ='userProfilePage'),
    path('Dashboard', views.DashboardPage, name ='DashboardPage'),
    path('schoolList', views.schoolList, name ='schoollist'),
    path('schoolAdd', views.schoolAdd, name ='schoolAdd'),
    path('schoolEdit/<str:id>', views.schoolEdit, name ='schoolEdit'),
    path('studentList', views.studentList, name ='studentlist'),
    path('studentAdd', views.studentAdd, name ='studentAdd'),
    path('studentEdit/<str:id>', views.studentEdit, name ='studentEdit'),
]
