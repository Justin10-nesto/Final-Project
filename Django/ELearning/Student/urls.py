
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
    path('updateStudent', views.updateStudent, name = 'updateStudent'),
    path('changePassword', views.changePassword, name = 'changePassword'),
    path('Dashboard', views.DashboardPage, name ='DashboardPage'),
    
    path('studentList', views.studentList, name ='studentlist'),
    path('studentAdd', views.studentAdd, name ='studentAdd'),
    path('studentEdit/<str:id>', views.studentEdit, name ='studentEdit'),
    path('studentDelete/<str:id>', views.studentDelete, name ='studentDelete'),

    path('TopicList/<str:sid>', views.TopicList, name ='Topiclist' ),
    path('TopicAdd/<str:sid>', views.TopicAdd, name ='TopicAdd'),
    path('TopicEdit/<str:sid>/<str:id>', views.TopicEdit, name ='TopicEdit'),
    path('TopicDelete/<str:sid>/<str:id>', views.TopicDelete, name ='TopicDelete'),

    path('ElearningPage/<str:sid>/<str:tid>', views.ElearningPage, name="ElearningPage"),

    path('booksPage/<str:sid>/<str:tid>', views.booksPage, name="booksPage"),
    path('BooksAdd/<str:sid>/<str:tid>', views.BooksAdd, name ='BooksAdd'),
    path('BooksEdit/<str:sid>/<str:tid>/<str:id>', views.BooksEdit, name ='BooksEdit'),
    path('BooksDelete/<str:sid>/<str:tid>/<str:id>', views.BooksDelete, name ='BooksDelete'),

    path('assigmentsPage/<str:sid>/<str:tid>', views.assigmentsPage, name="assigmentsPage"),
    path('AddAssigment/<str:sid>/<str:tid>', views.AssigmentsAdd, name="AddAssigment"),
    path('AssigmentsEdit/<str:sid>/<str:tid>/<str:id>', views.AssigmentsEdit, name ='AssigmentsEdit'),
    path('AssigmentsDelete/<str:sid>/<str:id>', views.AssigmentsDelete, name ='AssigmentsDelete'),

    path('AssigmentSubmision/<str:sid>/<str:tid>/<str:aid>', views.AssigmentSubmision, name = 'AssigmentSubmision'),
    path('UploadAssigments/<str:sid>/<str:tid>/<str:aid>', views.UploadAssigments, name="UploadAssigments"),
    path('marksAssigments/<str:sid>/<str:tid>/<str:aid>', views.marksAssigments, name="marksAssigments"),
    path('assignMarksToAssigment/<str:sid>/<str:tid>/<str:aid>', views.assignMarksToAssigment, name="assignMarksToAssigment"),
    path('AddAssigmentMarks/<str:sid>', views.AddAssigmentMarks, name="AddAssigmentMarks"),

    path('NotesPage/<str:sid>/<str:tid>', views.NotesPage, name="NotesPage"),
    path('NotesAdd/<str:sid>/<str:tid>', views.NotesAdd, name="NotesAdd"),

    path('discussionsPage/<str:sid>/<str:tid>', views.discussionsPage, name="discussionsPage"),

    path('groupsPage/<str:sid>/<str:tid>', views.groupsPage, name="groupsPage"),
    path('Addgroup/<str:sid>', views.groupAdd, name="Addgroup"),
    path('groupsEdit/<str:sid>/<str:id>', views.groupEdit, name ='groupsEdit'),
    path('groupsDelete/<str:sid>/<str:id>', views.groupDelete, name ='groupsDelete'),
 
    path('JoinToGroup/<str:id>', views.JoinToGroup, name="JoinToGroup"),
    path('RemoveStudentGroup/<str:gid>/<str:sid>', views.RemoveStudentGroup, name="RemoveStudentGroup"),
    path('LeftStudentGroup/<str:gid>', views.LeftStudentGroup, name="LeftStudentGroup"),
   
    path('groupContent/<str:id>', views.groupContent, name="groupContent"),
    path('groupPost/<str:id>', views.groupPost, name="groupPost"),
    path('groupPostLike/<str:id>', views.groupPostLikes, name="groupPostLikes"),
    path('AddGroupActivities/<str:gid>', views.AddGroupActivities, name="AddGroupActivities"),

    path('TutorialPage/<str:sid>/<str:tid>', views.TutorialPage, name="TutorialPage"),
    path('NextTuturial/<str:sid>/<str:tid>/<str:tuid>', views.NextTuturial, name="NextTuturial"),
    path('PreviousPage/<str:sid>/<str:tid>/<str:preid>', views.PreviousPage, name="PreviousPage"),
    path('TutorialAdd/<str:sid>/<str:tid>', views.TutorialAdd, name="TutorialAdd"),
    path('TutorialEdit/<str:sid>/<str:tid>/<str:tuid>', views.TutorialEdit, name="TutorialEdit"),

    path('anauncementPage/<str:sid>/<str:tid>', views.anauncementPage, name="anauncementPage"),
    path('anauncementContentPage/<str:sid>/<str:tid>/<str:anid>', views.anauncementContentPage, name="anauncementContentPage"),
    path('anauncementSoftDeletePage/<str:sid>/<str:tid>/<str:anid>', views.anauncementSoftDeletePage, name="anauncementSoftDeletePage"),
    path('ComposeAnaunciment/<str:sid>/<str:tid>', views.ComposeAnaunciment, name="ComposeAnaunciment"),
    path('anauncementSentPage/<str:sid>/<str:tid>', views.anauncementSentPage, name="anauncementSentPage"),
    path('anauncementTrashPage/<str:sid>/<str:tid>', views.anauncementTrashPage, name="anauncementTrashPage"),
 ]
