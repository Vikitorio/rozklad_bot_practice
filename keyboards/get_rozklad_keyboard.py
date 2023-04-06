from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from keyboards import group_list



def chose_faculty_group_arr(faculty):
    switcher = {
        'Фізики_та_Математики': group_list.fizmat_groups_arr,
        'Психології_Історії_Соціології': group_list.psychology_groups_arr,
        'Біології_Географії_Екології': group_list.biology_group_arr,
    }
    return switcher.get(faculty, "nothing")
class main_keyboard:
    def rozklad_panel(self):
        get_rozklad_button = KeyboardButton('/Отримати_Розклад')
        get_rozklad_file_button = KeyboardButton('/Отримати_Файл_Розкладу')
        option_button = KeyboardButton('/Налаштування')
        start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        start_keyboard.add(get_rozklad_button).add(get_rozklad_file_button)
        start_keyboard.add(option_button)
        return start_keyboard
    def options_panel(self):
        options_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        notification_button = KeyboardButton('/Нагадування')
        news_button = KeyboardButton('/Новини')
        delete_me_button = KeyboardButton('/Змінити_групу')
        main_menu_button = KeyboardButton('/Головне_меню')
        options_keyboard.add(main_menu_button).row(notification_button,news_button).add(delete_me_button)
        return options_keyboard
    def notification_panel(self):
        notification_options_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        set_notification_button = KeyboardButton('/Встановити_Нагадування')
        remove_notification_button = KeyboardButton('/Прибрати_Нагадування')
        main_menu_button = KeyboardButton('/Головне_меню')
        notification_options_keyboard.add(main_menu_button).row(set_notification_button,remove_notification_button)
        return notification_options_keyboard
    def news_panel(self):
        news_options_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        set_news_button = KeyboardButton('/Отримувати_Новини')
        remove_news_button = KeyboardButton('/Не_Отримувати_Новини')
        main_menu_button = KeyboardButton('/Головне_меню')
        news_options_keyboard.add(main_menu_button).row(set_news_button,remove_news_button)
        return news_options_keyboard
    def faculty_panel(self):
        faculty_fizmath = KeyboardButton('Фізики_та_Математики')
        faculty_psychology_history = KeyboardButton('Психології_Історії_Соціології')
        faculty_biology_geography_ecology = KeyboardButton('Біології_Географії_Екології')
        faculty_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        faculty_keyboard.add(faculty_fizmath).add(faculty_psychology_history).add(faculty_biology_geography_ecology)
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
                group_keyboard.add(KeyboardButton(group_arr[course-1][x]))
            else:
                group_keyboard.row(KeyboardButton(group_arr[course-1][x]),KeyboardButton(group_arr[course-1][x+1]))
        return group_keyboard
