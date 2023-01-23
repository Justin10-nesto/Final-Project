from django.shortcuts import render

# Create your views here.

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