from keyboards import group_list

def check_course(course):
    for item in group_list.course_arr:
        if course == item:
            return 1
    return 0
def check_faculty(faculty):
    for item in group_list.faculty_arr:
        if faculty == item:
            return 1
    return 0
def check_groupe(groupe):
    for item in group_list.all_group_arr:
        if groupe == item:
            return 1
    return 0
