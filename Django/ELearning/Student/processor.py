from Student.models import Student
from django.contrib.auth.models import User

def student(request):
    try:    
        user_id = request.user.id
        user = User.objects.filter(id = user_id).first() 
        student_data = Student.objects.filter(user=user).first()
        return {'student_data':student_data}
    
    except:
        return {'student_data':{}}
    