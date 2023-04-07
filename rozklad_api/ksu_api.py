import requests
import json
from datetime import date

base_url = 'https://ksu24.kspu.edu/api/'
def get_rozklad_api(groupe):
    response = requests.get(f'https://ksu24.kspu.edu/api/public_schedule/?group={groupe}')
    if response.status_code == 200:
        rezult = []
        subject_arr = response.json()
        for item in subject_arr:
            if str(item['date']) == str(date.today()) and check_group(groupe, item['student_groups']):
                try:
                    result_item = ''
                    #'online_id': '896 6125 9161', 'online_code': '51450761'
                    result_item = result_item + "Початок: " + item['time_begin'] + '\n'
                    result_item = result_item + item['discipline'] + '\n'
                    result_item = result_item + item['teacher'] + ' - ' + item['type'] + '\n'
                    if item['link'] != None:
                        result_item = result_item + str(item['link'])
                    else:
                        result_item = result_item + "ZoomId - " + item['online_id'] + ' | ' + 'pass - ' + item['online_code']
                    rezult.append(result_item)
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
    return False
