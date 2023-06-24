
from django.urls import path, include
from . import views, signals

urlpatterns = [
    # path('generating_exam', signals.generating_exam, name ='generating_exam'),
    path('convert/', views.convert_html_to_pdf, name='convert_html_to_pdf'),
    path('studentMarksPrediction', views.studentMarksPrediction, name ='studentMarksPrediction'),
    path('student_reults_progress', views.student_reults_progress, name ='student_reults_progress'),
    path('studentCourseRecomendation', views.studentCourseRecomendation, name ='studentCourseRecomendation'),
    path('analyze_logs', views.analyze_logs, name = "analyze_logs"),
    path('analyzing_studentPeformance/<str:id>', views.analyzing_studentPeformance, name = "analyzing_studentPeformance"),
    path('analyzingStudentFactorByMl', views.analyzingStudentFactorByMl, name= 'analyzingStudentFactorByMl'),
    path('api/studentResults', views.studentResults, name = 'studentResultsApi'),
    ]