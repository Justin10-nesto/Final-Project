from django.conf import settings
import numpy as np
import pandas as pd
import random
import datetime

# def O_level_timetable(o_level_subjects, selected_date):
#     timetable = []
#     start_time = [8,14]
#     total_subject = len(o_level_subjects)
#     o_level_subjects_copy  =total_subject
#     i=total_subject
#     while True:
#         total_subject = len(o_level_subjects)
#         index = random.randint(0,total_subject)
#         # try:
#         value = o_level_subjects[index-1]
#         print(value)

#         day = i//2
#         gemerated_date = datetime.datetime(selected_date.year, selected_date.month, selected_date.day) +datetime.datetime(0, 0, 1)
#         if i%2 == 0:
#             timetable.append(
#                 {'gemerated_date':gemerated_date,
#                 'seasion':'morning',
#                 'subject':value,

#                 'start_time': datetime.time(start_time[1], 0, 0),
#                 'end_time': datetime.time(start_time[1]+3, 0, 0)
#                 })
#         else:
#                 timetable.append(
#                 {'gemerated_date':gemerated_date,
#                 'seasion':'afternoon',
#                 'subject':value,
#                 'start_time': datetime.time(start_time[0], 0, 0),
#                 'end_time': datetime.time(start_time[0]+3, 0, 0)
#                 })
#         o_level_subjects.remove(value)

#         # except:
#         #     pass

#         i-=1

#         if i <=0:
#             break

#     value =o_level_subjects[0]
#     day = o_level_subjects_copy//2
#     gemerated_date = datetime.datetime(selected_date.year, selected_date.month, selected_date.day+day)

#     if o_level_subjects_copy%2 == 0:
#         timetable.append(
#         {'gemerated_date':gemerated_date,
#             'seasion':'morning',
#         'subject':value,
#         'start_time': datetime.time(start_time[1], 0, 0),
#         'end_time': datetime.time(start_time[1]+3, 0, 0)
#         })
#     else:
#         timetable.append(
#         {'gemerated_date':gemerated_date,
#         'seasion':'afternoon',
#         'subject':value,
#         'start_time': datetime.time(start_time[0], 0, 0),
#         'end_time': datetime.time(start_time[1]+3, 0, 0)
#         })
#     return timetable
# import random
# import datetime

def O_level_timetable(subjects, start_date):
    timetable = []
    total_subjects = len(subjects)
    sessions = ['morning', 'afternoon']
    time_slots = [[8, 11], [14, 17]]  # Start and end times for morning and afternoon sessions

    # Shuffle the subjects randomly
    random.shuffle(subjects)

    current_date = start_date

    for subject in subjects:
        # Skip weekends (Saturday and Sunday)
        while current_date.weekday() >= 5:
            current_date += datetime.timedelta(days=1)

        # Select a random session and time slot
        session = random.choice(sessions)
        time_slot = random.choice(time_slots)

        # Check if the current date is the last day of the month
        if current_date.month != (current_date + datetime.timedelta(days=1)).month:
            # If it is, update the current date to the first day of the next month
            current_date = current_date.replace(day=1) + datetime.timedelta(days=32)

        # Create a timetable entry for the subject
        timetable_entry = {
            'date': current_date,
            'session': session,
            'subject': subject,
            'start_time': datetime.time(time_slot[0], 0, 0),
            'end_time': datetime.time(time_slot[1], 0, 0)
        }

        # Append the timetable entry
        timetable.append(timetable_entry)

        # Update the current date
        current_date += datetime.timedelta(days=1)

    return timetable

def A_Level_timetable(comb):
    model_path = settings.STATICFILES_DIRS[0] +r'\csv files\advance.csv'
    data = pd.read_csv(model_path)
    course_data = data[data['course'] ==comb].iloc[0]
    # dumping data to an array
    subjects_data = []

    for i in range(1,5):
        subject_txt = 'Subjects'+str(i)
        subject_depa_txt = 'Subjects'+str(i)+ '_deparment'
        subjects_data.append({'subject':course_data[subject_txt],
                         'department':course_data[subject_depa_txt]})

    timetable = []
    start_time = [8,2]
    total_subject = len(subjects_data)
    subjects_data_copy  =total_subject
    i=total_subject
    while True:
        total_subject = len(subjects_data)
        index = random.randint(0,total_subject)
        print(index)
        try:
            value = subjects_data[index-1]
            subjects_data.remove(value)
            gemerated_date = datetime.datetime(selected_date.year, selected_date.month, selected_date.day+day)

            if i%2 == 0:
                timetable.append(
                    {'gemerated_date':gemerated_date,
                        'seasion':'morning',
                    'subject':value['subject'],
                    'start_time':start_time[1],
                    'end_time': start_time[1]+3
                    })
            else:
                    timetable.append(
                    {'gemerated_date':gemerated_date,
                    'seasion':'afternoon',
                    'subject':value['subject'],
                    'start_time':start_time[0],
                    'end_time': start_time[0]+3
                    })
        except:
            pass
        i-=1

        if i <=1:
            break

    value =subjects_data[0]
    if subjects_data_copy%2 == 0:
        timetable.append(
        {'gemerated_date':gemerated_date,
            'seasion':'morning',
        'subject':value['subject'],
        'start_time':start_time[1],
        'end_time': start_time[1]+3
        })
    else:
        timetable.append(
        {'gemerated_date':gemerated_date,
        'seasion':'afternoon',
        'subject':value['subject'],
        'start_time':start_time[0],
        'end_time': start_time[0]+3
        })
    return timetable
