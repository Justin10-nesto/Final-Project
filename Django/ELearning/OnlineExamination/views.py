from OnlineExamination.models import GPAClasses, Grade, Division, ExamType, QuestionsType, ExamFormat, Exam, StudentExam, StudentResult
from schools.models import Department, Subject, SchoolLevel, StudentClass, CourseSubject
from Student.models import Student, StudentSubject, Topic
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

def gradeList(request):
    Grades = Grade.objects.all()
    levels = SchoolLevel.objects.all()
    context = {'levels':levels, 'Grades':Grades}
    return render(request, 'OnlineExamination/gradeList.html', context)

def gradeAdd(request):
    if request.method == "POST":
        name = request.POST.get('name')
        lower_marks = request.POST.get('lower_marks')
        upper_marks = request.POST.get('upper_marks')
        weight = request.POST.get('weight')
        description = request.POST.get('description')
        level = request.POST.get('level')
        level_obj =SchoolLevel.objects.filter(id = level).first()
        Grade.objects.create(name=name, lower_marks=lower_marks, upper_marks=upper_marks, weight=weight, description=description, level=level_obj)
        return redirect('gradeList')
    
    levels = SchoolLevel.objects.all()
    context = {'levels':levels}
    return render(request, 'OnlineExamination/Add-Grades.html', context)


def gradeEdit(request, id):
    if request.method == "POST":
        name = request.POST.get('name')
        lower_marks = request.POST.get('lower_marks')
        upper_marks = request.POST.get('upper_marks')
        weight = request.POST.get('weight')
        description = request.POST.get('description')
        level = request.POST.get('level')
        level_obj =SchoolLevel.objects.filter(id = level).first()
        grade = Grade.objects.filter(id = id).first()
        grade.name=name
        grade.lower_marks=lower_marks
        grade.upper_marks=upper_marks
        grade.weight=weight
        grade.description=description
        grade.level=level_obj
        grade.save()
        return redirect('gradeList')
    
def gradeDelete(request, id):
    grade = Grade.objects.filter(id = id).first()
    grade.delete()
    return redirect('gradeList')
    
def divisionList(request):    
    divisions = Division.objects.all()
    levels = SchoolLevel.objects.all()
    context = {'levels':levels, 'divisions':divisions}
    return render(request, 'OnlineExamination/divisionList.html', context)

def divisionAdd(request):
    if request.method == "POST":
        name = request.POST.get('name')
        lower_point = request.POST.get('lower_point')
        upper_point = request.POST.get('upper_point')
        description = request.POST.get('description')
        level = request.POST.get('level')
        level_obj =SchoolLevel.objects.filter(id = level).first()
        Division.objects.create(name=name, lower_point=lower_point, upper_point=upper_point, description=description, level=level_obj)
        return redirect('divisionList')
    
    levels = SchoolLevel.objects.all()
    context = {'levels':levels}
    return render(request, 'OnlineExamination/Add-Divisions.html', context)


def divisionEdit(request, id):
    if request.method == "POST":
        name = request.POST.get('name')
        lower_point = request.POST.get('lower_point')
        upper_point = request.POST.get('upper_point')
        description = request.POST.get('description')
        level = request.POST.get('level')
        level_obj =SchoolLevel.objects.filter(id = level).first()
        division = Division.objects.filter(id = id).first()
        division.name=name
        division.lower_point=lower_point
        division.upper_point=upper_point
        division.description=description
        division.level=level_obj
        division.save()
        return redirect('divisionList')
    return redirect('divisionList')

def divisionDelete(request, id):
    division = Division.objects.filter(id = id).first()
    division.delete()
    return redirect('divisionList')
    

def examTypeList(request):
    examtypes = ExamType.objects.all()
    studentClass = StudentClass.objects.all()
    context = {'examtypes':examtypes, 'studentClass':studentClass}
    return render(request, 'OnlineExamination/examTypeList.html', context)

def examTypeAdd(request):
    if request.method == "POST":
        name = request.POST.get('name')
        weight_annual = request.POST.get('weight_annual')
        weight_final = request.POST.get('weight_final')
        studentClass = request.POST.get('studentClass')
        class_obj =StudentClass.objects.filter(id = studentClass).first()
        examType = ExamType.objects.create(name=name, weight_annual=weight_annual, weight_final=weight_final, studentClass=class_obj)
        return redirect('examTypeList')
    
    studentClass = StudentClass.objects.all()
    context = {'studentClass':studentClass}
    return render(request, 'OnlineExamination/Add-examType.html', context)


def examTypeEdit(request, id):
    if request.method == "POST":
        name = request.POST.get('name')
        weight_annual = request.POST.get('weight_annual')
        weight_final = request.POST.get('weight_final')
        studentClass = request.POST.get('studentClass')
        class_obj =StudentClass.objects.filter(id = studentClass).first()
        examType = ExamType.objects.filter(id = id).first()
        examType.name=name
        examType.weight_annual=weight_annual
        examType.weight_final=weight_final
        examType.studentClass=class_obj
        examType.save()
        return redirect('examTypeList')
    return redirect('examTypeList')

def examTypeDelete(request, id):
    examType = ExamType.objects.filter(id = id).first()
    examType.delete()
    return redirect('examTypeList')
    
def examList(request):
    context = {}
    return render(request, 'OnlineExamination/list-exam.html', context)

def MakeApointmentAdd(request):
        
    user_id = request.user.id
    user = User.objects.filter(id = user_id).first() 
    student_info = Student.objects.filter(user=user).first()
    student_subject = StudentSubject.objects.filter(student=student_info)
    context = {'student_subject':student_subject}
    return render(request, 'OnlineExamination/create appointment.html', context)

