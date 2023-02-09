from django.shortcuts import render, redirect
from django.conf import settings
import pandas as pd
from .models import Student
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import DefaultUsers
from schools.models import Subject
# Create your views here.
def UploadSelectedStudentPage(request):
    csv_path = settings.STATICFILES_DIRS[0] +r'\csv files\school.csv'
    data = pd.read_csv(csv_path)
    for index, row in data.iterrows():
        DefaultUsers.objects.create(number=row['number'], name=row['name'], school_selected=row['school_selected'], course=row['course'], type=row['type'], location=row['location'])
    return render(request, 'UAA/register.html')

def searchUserSelected(request):

    index_number = request.POST.get('index_number')
    user_info = DefaultUsers.objects.filter(number=index_number).first()
    context = {'user_info':user_info}
    return render(request, 'UAA/register.html', context)

def submitRegistration(request):
    if request.method == "POST":
        index_number = request.POST.get('index_number')
        email = request.POST.get('email')
        bod = request.POST.get('bod')
        class_level = request.POST.get('class_level')
        phone_no = request.POST.get('phone_no')
        password = request.POST.get('password')
        index_number = request.POST.get('index_number')
        User.objects.create_user(username=email, email=email, password=password)
        return redirect('loginPage')
    
def registerPage(request):
    return render(request, 'UAA/register.html')

def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')
        user =authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('DashboardPage')
        else:
            return redirect('loginPage')

    return render(request, 'UAA/login.html')

def logoutPage(request):
    logout(request)
    return redirect('loginPage')

def userProfilePage(request):
    return render(request, 'Admin/profile.html')

def DashboardPage(request):
    return render(request, 'Admin/dashboard.html')


def studentList(request):
    stud = Student.objects.all()
    context = {'stud':stud}
    return render(request, 'Admin/list-student.html', context)

def studentAdd(request):
    return render(request, 'Admin/add-student.html')

def studentEdit(request, id):
    return render(request, 'Admin/edit-student.html')

def examList(request):
    context = {}
    return render(request, 'Admin/list-exam.html', context)

def MakeApointmentAdd(request):
    return render(request, 'Admin/add-exam.html')

def ElearningPage(request, id):
    subject =Subject.objects.filter(id = id).first()
    context = {'subject':subject}
    return render(request, 'Student/elearning.html', context)

def NotesPage(request, id):
    subject =Subject.objects.filter(id = id).first()
    context = {'subject':subject}
    return render(request, 'Student/notes.html', context)
 

def booksPage(request, id):
    subject =Subject.objects.filter(id = id).first()
    context = {'subject':subject}
    return render(request, 'Student/books.html', context)
 
def assigmentsPage(request, id):
    subject =Subject.objects.filter(id = id).first()
    context = {'subject':subject}
    return render(request, 'Student/assigments.html', context)

def AddAssigment(request, sid):
    subject =Subject.objects.filter(id = sid).first()
    context = {'subject':subject}
    return render(request, 'Student/.add-assigmnents.html', context)

def UploadAssigments(request, sid, aid):
    subject =Subject.objects.filter(id = sid).first()
    context = {'subject':subject}
    return render(request, 'Student/assigment-upload.html', context)

def marksAssigments(request, sid, aid):
    subject =Subject.objects.filter(id = sid).first()
    context = {'subject':subject}
    return render(request, 'Student/assigment-marks.html', context)

def AddAssigmentMarks(request, sid):
    subject =Subject.objects.filter(id = sid).first()
    context = {'subject':subject}
    return render(request, 'Student/add-assigmnents-marks.html', context)

def discussionsPage(request, id):
    subject =Subject.objects.filter(id = id).first()
    context = {'subject':subject}
    return render(request, 'Student/discussions.html', context)
 
def groupsPage(request, id):
    subject =Subject.objects.filter(id = id).first()
    context = {'subject':subject}
    return render(request, 'Student/groups.html', context)
 
def anauncementPage(request, id):
    subject =Subject.objects.filter(id = id).first()
    context = {'subject':subject}
    return render(request, 'Student/anauncement.html', context)