import os
def get_file(dir):
    dir_path = f"D:\\rozklad_bot\\Розклади_ексель\\{dir}\\documents"
    files = os.listdir(dir_path)
    first_file = os.path.join(dir_path, files[0])
    return first_file
def cleane_the_dir(dir):
    dir_path = f"D:\\rozklad_bot\\Розклади_ексель\\{dir}\\documents"
    for file_name in os.listdir(dir_path):
        # Construct the full file path
        file_path = os.path.join(dir_path, file_name)

        # Check if the file is a file (not a directory) and delete it
        if os.path.isfile(file_path):
            os.remove(file_path)
