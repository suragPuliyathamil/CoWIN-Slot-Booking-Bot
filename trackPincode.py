# importing the requests library
import requests
import time
import os
from datetime import date
from datetime import datetime
# api-endpoint
pincodes = ['670613',
            '670650',
            '670642',
            '670691',
            '670702',
            '670692',
            '673316',
            '670102',
            '670643',
            '670741',
            '670593',
            '670007',
            '670703']

date_var = date.today().strftime("%d-%m-%Y")

def notify(title, subtitle, message):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    os.system('terminal-notifier {}'.format(' '.join([m, t, s])))

# sending get request and saving the response as response object
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}

while True:
    time.sleep(4)
    for pincode in pincodes:
        URL = "http://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=" + pincode + "&date=" + date_var
        try:
            r = requests.get(url=URL, headers=headers)
        except requests.ConnectionError:
            print("No Network at " + str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
            continue
        print(r.status_code)
        data = r.json()

        flag = 0

        for center in data['centers']:
            for session in center['sessions']:
                if session['available_capacity'] > 0 and session['min_age_limit'] < 45 and session['vaccine'] == 'COVAXIN':
                    notify(center['name'],'Vaccine available','Opening Browse')
                    print(center['name'])
                    flag = 1
        if flag == 0:
            print("Not available at " + str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
