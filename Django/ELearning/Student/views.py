from django.shortcuts import render, redirect
from django.conf import settings
import pandas as pd
from django.contrib.auth.models import User
from .models import DefaultUsers
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
    return render(request, 'UAA/login.html')

def userProfilePage(request):
    return render(request, 'Admin/profile.html')

def DashboardPage(request):
    return render(request, 'Admin/dashboard.html')

def schoolList(request):
    return render(request, 'Admin/list-school.html')

def schoolAdd(request):
    return render(request, 'Admin/add-school.html')

def schoolEdit(request, id):
    return render(request, 'Admin/edit-school.html')

def studentList(request):
    return render(request, 'Admin/list-student.html')

def studentAdd(request):
    return render(request, 'Admin/add-student.html')

def studentEdit(request, id):
    return render(request, 'Admin/edit-student.html')