from django.contrib import admin

# Register your models here.
from OnlineExamination.models import GPAClasses, Grade, Division, ExamType, QuestionsType, ExamFormat, StudentExam, StudentResult


admin.site.register(GPAClasses)
admin.site.register(Grade)
admin.site.register(Division)
admin.site.register(ExamType)
admin.site.register(QuestionsType)
admin.site.register(ExamFormat)
admin.site.register(StudentExam)
admin.site.register(StudentResult)
