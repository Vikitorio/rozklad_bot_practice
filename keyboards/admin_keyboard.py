from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from keyboards import group_list
def chose_faculty_group_arr(faculty):
    switcher = {
        'Фізики_та_Математики': group_list.fizmat_groups_arr,
        'Психології_Історії_Соціології': group_list.psychology_groups_arr,
        'Біології_Географії_Екології': group_list.biology_group_arr,
    }
    return switcher.get(faculty, "nothing")
class main_admin_keyboard:
    def main_panel(self):
        get_rozklad_button = KeyboardButton('/Додати_Розклад')
        get_rozklad_file_button = KeyboardButton('/Відправити_Новину')
        option_button = KeyboardButton('/Головне_меню')
        start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        start_keyboard.add(get_rozklad_button).add(get_rozklad_file_button)
        start_keyboard.add(option_button)
        return start_keyboard

    def faculty_panel(self,additional_choise = 0):
        additional_button = KeyboardButton('Всім')
        cansel_b = KeyboardButton('/Скасувати_Операцію')
        faculty_fizmath = KeyboardButton('Фізики_та_Математики')
        faculty_psychology_history = KeyboardButton('Психології_Історії_Соціології')
        faculty_biology_geography_ecology = KeyboardButton('Біології_Географії_Екології')
        faculty_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        if additional_choise ==1:
            faculty_keyboard.add(additional_button)
        faculty_keyboard.add(faculty_fizmath).add(faculty_psychology_history).add(faculty_biology_geography_ecology).add(cansel_b)
        return faculty_keyboard

    def group_course(self,additional_choise = 0):
        additional_button = KeyboardButton('Всім')
        first_course = KeyboardButton('1')
        second_course = KeyboardButton('2')
        third_course = KeyboardButton('3')
        fourth_course = KeyboardButton('4')
        first_m_course = KeyboardButton('1-магістр')
        second_m_course = KeyboardButton('2-магістр')
        group_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        if additional_choise ==1:
            group_keyboard.add(additional_button)
        group_keyboard.row(first_course, second_course).row(third_course, fourth_course).row(first_m_course,
                                                                                             second_m_course)
        group_keyboard.add(KeyboardButton('/Скасувати_Операцію'))
        return group_keyboard

    def get_groups_panel(self, faculty, course,additional_choise = 0):
        additional_button = KeyboardButton('Всім')
        group_arr = chose_faculty_group_arr(faculty)
        group_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        if course == '1-магістр':
            course = 5
        elif course == '2-магістр':
            course = 6
        if additional_choise ==1:
            group_keyboard.add(additional_button)
        for x in range(0, len(group_arr[course - 1]), 2):
            print(x)
            if (len(group_arr[course - 1]) - (x)) < 2:
                group_keyboard.add(KeyboardButton(group_arr[course - 1][x]))
            else:
                group_keyboard.row(KeyboardButton(group_arr[course - 1][x]),
                                   KeyboardButton(group_arr[course - 1][x + 1]))
        group_keyboard.add(KeyboardButton('/Скасувати_Операцію'))
        return group_keyboard