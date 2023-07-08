import numpy as np

def getting_points(grades, marks):
    point_exam = {'point':[], 'grade':[]}
    for mark in marks:
        for grade in grades:
            if grade.upper_marks >= mark and grade.lower_marks <= mark:
                point_exam['point'].append(grade.weight)
                point_exam['grade'].append(grade.name)
    return point_exam

def gettingGrade(grades, mark):
    grade_obtained = ''
    for grade in grades:
        if grade.upper_marks >= mark and grade.lower_marks <= mark:
            grade_obtained = grade.name
    return grade_obtained

def getting_pass_subject(points, level):
    if level  == 'O-Level':
        points.sort()
        array_points = np.array(points[:7])
    else:
        array_points = points
    total_points = array_points.sum()
    return total_points

def checking_division(total_points, divisions):
    name = ''
    for division in divisions:
        if division.upper_point >= total_points  and division.lower_point <= total_points:
            name = division.name
    return name

def getting_average(marks):
    markss_arr = np.array(marks)
    average = markss_arr.mean()
    return average

def getting_student_dropdown(marks):
    markss_arr = np.array(marks)
    std = markss_arr.std()
    return std


# marks = [57,90,89,78,45,56,57,98,45,46,56]
# points=getting_points(marks=marks)
# pass_subject = getting_pass_subject(points['point'], )
# division = checking_division(pass_subject)
# average = getting_average(marks)
# grade = getting_points([average, average])
# print(average)
# print(grade['grade'][0])
# print(division[1])
# print(getting_student_dropdown(marks))