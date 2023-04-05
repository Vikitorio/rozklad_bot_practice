import requests
import json
from datetime import date

base_url = 'https://ksu24.kspu.edu/api/'
def get_rozklad_api(groupe):
    response = requests.get('https://ksu24.kspu.edu/api/public_schedule/?group=07-142')
    if response.status_code ==200:
        print(response.json())
        rezult = []
        subject_arr = response.json()
        for item in subject_arr:
            if item['date'] == date.today() and check_group(groupe, item['student_groups']):
                try:
                    result_item = ''
                    result_item = result_item + "Початок: " + item['time_begin']
                    result_item = result_item + item['teacher'] + ' ' + item['type'] + '\n'
                    result_item = result_item + item['discipline'] + '\n'
                    result_item = result_item + item['link']
                    rezult.append(result_item )
                except:
                    print()
        if len(rezult) == 0:
            rezult.append('В мене немає інформації про пари сьогодні, зверніться до старости')
        return rezult
    else:
        0





def check_group(groupe, arr):
    for x in arr:
        if x['name'] == groupe:
            return True
        else:
            return False
