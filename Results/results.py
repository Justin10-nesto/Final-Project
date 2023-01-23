import numpy as np
Ilower =7
IIlower = 18
IIIlower = 24
IVlower = 26
Olower = 34
Iupper =17
IIupper = 22
IIIupper = 25
IVupper = 32
Oupper =  35
Alower =80
Blower = 60
Clower = 50
Dlower = 35
Flower = 0
Aupper =100
Bupper = 79
Cupper = 59
Dupper = 50
Oupper =  35

def getting_points(marks):
    point_exam = {'point':[], 'grade':[]}
    for mark in marks:
        if Alower <= mark  and Aupper >= mark:
            point_exam['point'].append(1)
            point_exam['grade'].append('A')
        elif Blower <= mark  and Bupper >= mark:
            point_exam['point'].append(2)
            point_exam['grade'].append('B')
    
        elif Clower <= mark  and Cupper >= mark:
        
            point_exam['point'].append(3)
            point_exam['grade'].append('C')
            
        elif Dlower <= mark  and Dupper >= mark:
        
            point_exam['point'].append(4)
            point_exam['grade'].append('D')
            
        elif Flower <= mark  and Fupper >= mark:
            
            point_exam['point'].append(F)
            point_exam['grade'].append('F')
        else:
            point_exam['point'].append(0)
            point_exam['grade'].append('INC')
    return point_exam

def getting_pass_subject(points):
    points.sort()
    array_points = np.array(points[:7])
    total_points = array_points.sum()
    return total_points

def checking_division(total_points):
    if Ilower <= total_points  and Iupper >= total_points:
        return 'I', total_points
    
    elif IIlower <= total_points  and IIupper >= total_points:
        return 'II', total_points
    
    elif IIIlower <= total_points  and IIIupper >= total_points:
        return 'III', total_points
    
    elif IVlower <= total_points  and IVupper >= total_points:
        return 'IV', total_points
    
    elif Olower <= total_points  and Oupper >= total_points:
        return 'O', total_points
    else:
        return 'INC', 'Not Exist'
    
def getting_average(marks):
    marks_arr = np.array(marks)
    average = marks_arr.mean()
    return average

def getting_student_dropdown(marks):
    marks_arr = np.array(marks)
    std = marks_arr.std()
    return std


marks = [57,90,89,78,45,56,57,98,45,46,56]
points=getting_points(marks=marks)
pass_subject = getting_pass_subject(points['point'])
division = checking_division(pass_subject)
average = getting_average(marks)
grade = getting_points([average, average])
print(average)
print(grade['grade'][0])
print(division[1])
print(getting_student_dropdown(marks))