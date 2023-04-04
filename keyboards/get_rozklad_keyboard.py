from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

fizmat_groups_arr = [['12-111','12-112','12-121','12-131','12-132','12-141','12-161'],
                     ['12-211','12-212','12-221','12-231','12-232','12-241','12-261'],
                     ['12-311','12-321','12-331','12-332','12-341','12-361'],
                     ['12-411','12-421','12-431','12-432','12-441','12-461'],
                     ['12-111м','12-121м','12-131м','12-132м','12-141м','12-161м'],
                     ['12-211м','12-221м','12-231м','12-232м','12-241м','12-261м']]


def chose_faculty_group_arr(faculty):
    switcher = {
        'Фіз-мат': fizmat_groups_arr,
        1: "one",
        2: "two",
    }
    return switcher.get(faculty, "nothing")
class main_keyboard:
    def rozklad_panel(self):
        get_rozklad_button = KeyboardButton('/Отримати_Розклад')
        option_button = KeyboardButton('/Налаштування')
        start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        start_keyboard.add(get_rozklad_button)
        start_keyboard.add(option_button)
        return start_keyboard
    def options_panel(self):
        options_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        notification_button = KeyboardButton('/Авто_Нагадування')
        main_menu_button = KeyboardButton('/Головне_меню')
        options_keyboard.add(notification_button).add(main_menu_button)
        return options_keyboard
    def faculty_panel(self):
        faculty_fizmath = KeyboardButton('Фіз-мат')
        faculty_sport = KeyboardButton('Спорт')
        faculty_medicine = KeyboardButton('Медицина')
        faculty_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        faculty_keyboard.add(faculty_fizmath).add(faculty_sport).add(faculty_medicine)
        return faculty_keyboard


    def group_course(self):
        first_course = KeyboardButton('1')
        second_course = KeyboardButton('2')
        third_course = KeyboardButton('3')
        fourth_course = KeyboardButton('4')
        first_m_course = KeyboardButton('1-магістр')
        second_m_course = KeyboardButton('2-магістр')
        group_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        group_keyboard.add(KeyboardButton('/Скасувати'))
        group_keyboard.row(first_course,second_course ).row(third_course,fourth_course).row(first_m_course,second_m_course)
        return group_keyboard


    def get_groups_panel(self, faculty, course):
        group_arr = chose_faculty_group_arr(faculty)
        group_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        group_keyboard.add(KeyboardButton('/Скасувати'))
        if course == '1-магістр':
            course = 5
        elif course == '2-магістр':
            course = 6
        for x in range(0,len(group_arr[course-1]),2):
            print (x)
            if (len(group_arr[course-1])-(x)) < 2:
                print("1-if")
                group_keyboard.add(KeyboardButton(group_arr[course-1][x]))
            else:
                print("2-if")
                group_keyboard.row(KeyboardButton(group_arr[course-1][x]),KeyboardButton(group_arr[course-1][x+1]))
        return group_keyboard
