from keyboards import group_list

def check_course(course):
    for item in group_list.course_arr:
        if course == "Всім":
            return 1
        if course == item:
            return 1
    return 0
def check_faculty(faculty):
    for item in group_list.faculty_arr:
        if faculty == "Всім":
            return 1
        if faculty == item:
            return 1
    return 0
def check_groupe(groupe):
    for item in group_list.all_group_arr:
        for item_item in item:
            if groupe == "Всім":
                return 1
            if groupe == item_item:
                return 1
    return 0
