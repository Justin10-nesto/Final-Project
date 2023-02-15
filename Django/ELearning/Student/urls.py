
from django.urls import path, include
from . import views
urlpatterns = [
    
    path('', views.loginPage, name='loginPage'),
    path("logoutPage", views.logoutPage, name="logoutPage"),
    path('searchUserSelected', views.searchUserSelected, name = "searchUserSelected"),
    path('UploadSelectedStudentPage', views.UploadSelectedStudentPage, name = "UploadSelectedStudentPage"),
    path('register', views.registerPage, name ='registerPage'),
    path('submitRegistration', views.submitRegistration, name = 'submitRegistration'),
    path('userProfile', views.userProfilePage, name ='userProfilePage'),
   
    path('Dashboard', views.DashboardPage, name ='DashboardPage'),
    path('studentList', views.studentList, name ='studentlist'),
    path('studentAdd', views.studentAdd, name ='studentAdd'),
    path('studentEdit/<str:id>', views.studentEdit, name ='studentEdit'),
    path('studentDelete/<str:id>', views.studentDelete, name ='studentDelete'),

    path('examList', views.examList, name = 'examList'),
    path('MakeApointmentAdd', views.MakeApointmentAdd, name = 'MakeApointmentAdd'),
    
    path('TopicList/<str:sid>', views.TopicList, name ='Topiclist' ),
    path('TopicAdd/<str:sid>', views.TopicAdd, name ='TopicAdd'),
    path('TopicEdit/<str:sid>/<str:id>', views.TopicEdit, name ='TopicEdit'),
    path('TopicDelete/<str:sid>/<str:id>', views.TopicDelete, name ='TopicDelete'),

    path('ElearningPage/<str:sid>/<str:tid>', views.ElearningPage, name="ElearningPage"),
    
    path('booksPage/<str:sid>/<str:tid>', views.booksPage, name="booksPage"),
    path('BooksAdd/<str:sid>/<str:tid>', views.BooksAdd, name ='BooksAdd'),
    path('BooksEdit/<str:sid>/<str:tid>/<str:id>', views.BooksEdit, name ='BooksEdit'),
    path('BooksDelete/<str:sid>/<str:id>', views.BooksDelete, name ='BooksDelete'),

    path('assigmentsPage/<str:sid>/<str:tid>', views.assigmentsPage, name="assigmentsPage"),
    path('AddAssigment<str:sid>/<str:tid>', views.AssigmentsAdd, name="AddAssigment"),
    path('AssigmentsEdit/<str:sid>/<str:tid>/<str:id>', views.AssigmentsEdit, name ='AssigmentsEdit'),
    path('AssigmentsDelete/<str:sid>/<str:id>', views.AssigmentsDelete, name ='AssigmentsDelete'),

    
    path('UploadAssigments/<str:sid>/<str:tid>/<str:aid>', views.UploadAssigments, name="UploadAssigments"),
    path('marksAssigments/<str:sid>/<str:aid>', views.marksAssigments, name="marksAssigments"),
    path('AddAssigmentMarks/<str:sid>', views.AddAssigmentMarks, name="AddAssigmentMarks"),

    path('NotesPage/<str:sid>/<str:tid>', views.NotesPage, name="NotesPage"),
    path('discussionsPage/<str:sid>/<str:tid>', views.discussionsPage, name="discussionsPage"),
    path('groupsPage/<str:sid>/<str:tid>', views.groupsPage, name="groupsPage"),
    path('anauncementPage/<str:sid>/<str:tid>', views.anauncementPage, name="anauncementPage"),
]
