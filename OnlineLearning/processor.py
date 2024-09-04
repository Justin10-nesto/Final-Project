from OnlineLearning.models import Student, Teacher
from django.contrib.auth.models import User

def student(request):
    try:    
        user_id = request.user.id
        teacher_data = {}
        student_data = {}
        user = User.objects.filter(id = user_id).first() 
        student = Student.objects.filter(user=user)
        teacher = Teacher.objects.filter(user=user)
        student = Student.objects.filter(user=user)
        if student.exists():
            student_data = student.first()
        if teacher.exists():
            teacher_data = teacher.first()
        return {'student_data':student_data, 'teacher_data':teacher_data}
    
    except:
        return {'student_data':{}}
    