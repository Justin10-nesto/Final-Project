from django.shortcuts import render, redirect
from .models import School, Domain, Department, Subject, SchoolLevel, StudentClass
from django_tenants.utils import schema_context

def view_schools(request, id):
    school_info = School.objects.filter(id = id).first()
    context = {'school_info':school_info}
    return render(request, 'UAA/view-school.html', context)

def schoolList(request): 
    school_info = School.objects.all()
    context = {'school_info':school_info}
    return render(request, 'Admin/list-school.html', context)

def schoolAdd(request):
    if request.method == "POST":
        school_name = request.POST.get('school_name')
        schoo_logo = request.POST.get('schoo_logo')
        school_level = request.POST.get('school_level')
        school_adress = request.POST.get('school_adress')
        head_of_school = request.POST.get('head_of_school')
        school_domain = request.POST.get('school_domain')
        school_obj =School(schema_name = school_name, school_name= school_name,schoo_logo =schoo_logo, school_level= school_level, school_adress =school_adress, head_of_school = head_of_school)
        school_obj.save()
        domain = Domain()
        domain.domain = school_domain # don't add your port or www here! on a local server you'll want to use localhost here
        domain.tenant = school_obj
        domain.is_primary = True
        domain.save()
        return redirect('schoollist')
    context ={}
    return render(request, 'Admin/add-school.html', context)

def schoolEdit(request, id):
    context = {}
    return render(request, 'Admin/edit-school.html', context)

def schoolDelete(request, id):
    School.objects.filter(id = id).first().delete()
    return redirect('schoollist')

def DepartmentList(request):
    department = Department.objects.all()
    context = {'department':department}
    return render(request, 'Admin/list-department.html', context)

def DepartmentAdd(request):
    if request.method == "POST":
        department_name = request.POST.get('department_name')
        department_start_date = request.POST.get('department_start_date')
        department_Hod = request.POST.get('department_Hod')
        
        depart = Department(name=department_name, department_Hod=department_Hod, start_date=department_start_date)
        depart.save()
        return redirect('Departmentlist')
    return render(request, 'Admin/add-department.html')

def DepartmentEdit(request, id):
    if request.method == "POST":
        department_name = request.POST.get('department_name')
        department_start_date = request.POST.get('department_start_date')
        department_Hod = request.POST.get('department_Hod')
        department = Department.objects.filter(id=id).first()
        department.name=department_name
        department.department_Hod=department_Hod
        department.start_date=department_start_date
        department.save()
        return redirect('Departmentlist')
    
    department = Department.objects.filter(id=id).first()
    context = {'department':department}
    return render(request, 'Admin/edit-department.html', context)

def DepartmentDelete(request, id):
    Department.objects.filter(id = id).first().delete()
    return redirect('Departmentlist')


def SubjectList(request):
    Subjects = Subject.objects.all()
    context = {'Subjects':Subjects}
    return render(request, 'Admin/list-subject.html', context)

def SubjectAdd(request):
    if request.method == "POST":
        subject_code = request.POST.get('subject_code')
        subject_name = request.POST.get('subject_name')
        department = request.POST.get('department')
        department_selected = Department.objects.filter(id=department).first()
        subject = Subject(subject_code =subject_code, subject_name=subject_name)
        subject.department = department_selected
        subject.save()
        return redirect('Subjectlist')
    department = Department.objects.all()
    context = {'department':department}
  
    return render(request, 'Admin/add-subject.html', context)

def SubjectEdit(request, id):
    if request.method == "POST":
        subject_code = request.POST.get('subject_code')
        subject_name = request.POST.get('subject_name')
        department = request.POST.get('department')
        Subject_obj = Subject.objects.filter(id=id).first()

        department_selected = Department.objects.filter(id=department).first()
        Subject_obj.subject_code = subject_code
        Subject_obj.subject_name = subject_name
        Subject_obj.department = department_selected
        subect_obj.save()
        return redirect('Subjectlist')
    
    Subject = Subject.objects.filter(id=id).first()
    context = {'Subject':Subject}
    return render(request, 'Admin/edit-subject.html', context)

def SubjectDelete(request, id):
    subject =Subject.objects.filter(id = id).first()
    subject.delete()
    return redirect('Subjectlist')


def SchoolLevelList(request):
    schoolLevels = SchoolLevel.objects.all()
    context = {'schoolLevels':schoolLevels}
    return render(request, 'Admin/list-SchoolLevel.html', context)

def SchoolLevelAdd(request):
    if request.method == "POST":
        name = request.POST.get('name')
        schoolLevel = SchoolLevel.objects.create(name=name)
        return redirect('SchoolLevellist')
    department = Department.objects.all()
    context = {'department':department}
  
    return render(request, 'Admin/add-SchoolLevel.html', context)

def SchoolLevelEdit(request, id):
    if request.method == "POST":
        name = request.POST.get('name')
        SchoolLevel_obj = SchoolLevel.objects.filter(id=id).first()
        SchoolLevel_obj.name = name
        SchoolLevel_obj.save()
        return redirect('SchoolLevellist')
    
    schoolLevel = SchoolLevel.objects.filter(id=id).first()
    context = {'schoolLevel':schoolLevel}
    return render(request, 'Admin/edit-SchoolLevel.html', context)

def SchoolLevelDelete(request, id):
    schoolLevel =SchoolLevel.objects.filter(id = id).first()
    schoolLevel.delete()
    return redirect('SchoolLevellist')


def StudentClassList(request):
    studentClasss = StudentClass.objects.all()
    context = {'studentClasss':studentClasss}
    return render(request, 'Admin/list-StudentClass.html', context)

def StudentClassAdd(request):
    if request.method == "POST":
        name = request.POST.get('name')
        level = request.POST.get('level')
        level_obj = SchoolLevel.objects.filter(id = level).first()
        StudentClass.objects.create(name=name, level=level_obj)
        return redirect('StudentClasslist')
    schoolLevels = SchoolLevel.objects.all()
    context = {'schoolLevels':schoolLevels}
  
    return render(request, 'Admin/add-StudentClass.html', context)

def StudentClassEdit(request, id):
    if request.method == "POST":
        name = request.POST.get('name')
        level = request.POST.get('level')
        level_obj = SchoolLevel.objects.filter(id = level).first()
        StudentClass_obj = StudentClass.objects.filter(id=id).first()
        
        level = StudentClass_obj.update(name = name, level=level_obj)
        level.save()
        return redirect('StudentClasslist')
    
    schoolLevels = SchoolLevel.objects.all()
    studentClass = StudentClass.objects.filter(id=id).first()
    context = {'studentClass':studentClass, 'schoolLevels':schoolLevels}
    return render(request, 'Admin/edit-StudentClass.html', context)

def StudentClassDelete(request, id):
    studentClass =StudentClass.objects.filter(id = id).first()
    studentClass.delete()
    return redirect('StudentClasslist')