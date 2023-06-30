
from django.urls import path, include
from . import views
urlpatterns = [
    path('view_schools', views.view_schools, name ='view_schools'),

    path('schoolList', views.schoolList, name ='schoollist' ),
    path('schoolAdd', views.schoolAdd, name ='schoolAdd'),
    path('schoolEdit/<str:id>', views.schoolEdit, name ='schoolEdit'),
    path('schoolDelete/<str:id>', views.schoolDelete, name ='schoolDelete'),

    path('DepartmentList', views.DepartmentList, name ='Departmentlist'),
    path('DepartmentAdd', views.DepartmentAdd, name ='DepartmentAdd'),
    path('DepartmentEdit/<str:id>', views.DepartmentEdit, name ='DepartmentEdit'),
    path('DepartmentDelete/<str:id>', views.DepartmentDelete, name ='DepartmentDelete'),

    path('SubjectRegistration', views.SubjectRegistration, name ='SubjectRegistration'),
    path('Curruculum', views.Curruculum, name ='Curruculum'),
    path('SubjectList', views.SubjectList, name ='Subjectlist'),
    path('SubjectAdd', views.SubjectAdd, name ='SubjectAdd'),
    path('SubjectEdit/<str:id>', views.SubjectEdit, name ='SubjectEdit'),
    path('SubjectDelete/<str:id>', views.SubjectDelete, name ='SubjectDelete'),

    path('SchoolLevelList', views.SchoolLevelList, name ='SchoolLevellist'),
    path('SchoolLevelAdd', views.SchoolLevelAdd, name ='SchoolLevelAdd'),
    path('SchoolLevelEdit/<str:id>', views.SchoolLevelEdit, name ='SchoolLevelEdit'),
    path('SchoolLevelDelete/<str:id>', views.SchoolLevelDelete, name ='SchoolLevelDelete'),

    path('StudentClassList', views.StudentClassList, name ='StudentClasslist'),
    path('StudentClassAdd', views.StudentClassAdd, name ='StudentClassAdd'),
    path('StudentClassEdit/<str:id>', views.StudentClassEdit, name ='StudentClassEdit'),
    path('StudentClassDelete/<str:id>', views.StudentClassDelete, name ='StudentClassDelete'),

    path('CourseList', views.CourseList, name ='Courselist'),
    path('CourseAdd', views.CourseAdd, name ='CourseAdd'),
    path('CourseEdit/<str:id>', views.CourseEdit, name ='CourseEdit'),
    path('CourseDelete/<str:id>', views.CourseDelete, name ='CourseDelete'),

]
