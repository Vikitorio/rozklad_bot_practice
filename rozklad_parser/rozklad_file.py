import os
def get_file(dir):
    dir_path = f"D:\\rozklad_bot\\Розклади_ексель\\{dir}"
    files = os.listdir(dir_path)
    first_file = os.path.join(dir_path, files[0])
    return first_file

get_file('Фізики_та_Математики')