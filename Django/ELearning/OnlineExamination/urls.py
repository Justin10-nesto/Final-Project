
from django.urls import path, include
from . import views
urlpatterns = [
    path('gradeList', views.gradeList, name = 'gradeList'),
    path('gradeAdd', views.gradeAdd, name ='gradeAdd'),
    path('gradeEdit/<str:id>', views.gradeEdit, name ='gradeEdit'),
    path('gradeDelete/<str:id>', views.gradeDelete, name ='gradeDelete'),
   
    path('divisionList', views.divisionList, name = 'divisionList'),
    path('divisionAdd', views.divisionAdd, name ='divisionAdd'),
    path('divisionEdit/<str:id>', views.divisionEdit, name ='divisionEdit'),
    path('divisionDelete/<str:id>', views.divisionDelete, name ='divisionDelete'),
  
    path('examTypeList', views.examTypeList, name = 'examTypeList'),
    path('examTypeAdd', views.examTypeAdd, name ='examTypeAdd'),
    path('examTypeEdit/<str:id>', views.examTypeEdit, name ='examTypeEdit'),
    path('examTypeDelete/<str:id>', views.examTypeDelete, name ='examTypeDelete'),
      
    path('examList', views.examList, name = 'examList'),
    path('MakeApointmentAdd', views.MakeApointmentAdd, name = 'MakeApointmentAdd'),

]
