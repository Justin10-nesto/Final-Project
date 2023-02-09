
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.loginPage, name='loginPage'),
    path("logoutPage", views.logoutPage, name="logoutPage"),
    path('searchUserSelected', views.searchUserSelected, name = "searchUserSelected"),
    path('register', views.registerPage, name ='registerPage'),
    path('submitRegistration', views.submitRegistration, name = 'submitRegistration'),
    path('userProfile', views.userProfilePage, name ='userProfilePage'),
   
    path('Dashboard', views.DashboardPage, name ='DashboardPage'),
    path('studentList', views.studentList, name ='studentlist'),
    path('studentAdd', views.studentAdd, name ='studentAdd'),
    path('studentEdit/<str:id>', views.studentEdit, name ='studentEdit'),
    
    path('examList', views.examList, name = 'examList'),
    path('MakeApointmentAdd', views.MakeApointmentAdd, name = 'MakeApointmentAdd'),
    
    path('ElearningPage/<str:id>', views.ElearningPage, name="ElearningPage"),
    path('booksPage/<str:id>', views.booksPage, name="booksPage"),
    
    path('assigmentsPage/<str:id>', views.assigmentsPage, name="assigmentsPage"),
    path('AddAssigment/<str:sid>', views.AddAssigment, name="AddAssigment"),
    path('UploadAssigments/<str:sid>/<str:aid>', views.UploadAssigments, name="UploadAssigments"),
    path('marksAssigments/<str:sid>/<str:aid>', views.marksAssigments, name="marksAssigments"),
    path('AddAssigmentMarks/<str:sid>', views.AddAssigmentMarks, name="AddAssigmentMarks"),

    path('NotesPage/<str:id>', views.NotesPage, name="NotesPage"),
    path('discussionsPage/<str:id>', views.discussionsPage, name="discussionsPage"),
    path('groupsPage/<str:id>', views.groupsPage, name="groupsPage"),
    path('anauncementPage/<str:id>', views.anauncementPage, name="anauncementPage"),
]
