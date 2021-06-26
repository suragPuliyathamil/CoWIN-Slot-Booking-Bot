from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
from PyQt5 import Qt
import sys
import socket
import requests
import os
from datetime import date
from datetime import datetime
# api-endpoint
def DisplayNot(text):
	#print(text)
	data = text.split(" ")
	if len(data)>6 :
		return data[6][:-1]
	# if data:
	# 	return data
	return 0

def notify(title, subtitle, message):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    os.system('terminal-notifier {}'.format(' '.join([m, t, s])))

def bookVaccine(pincode):
	driver = webdriver.Chrome('/Users/surag/Desktop/Vaccine_Tracker-main/chromedriver')
	driver.get('https://selfregistration.cowin.gov.in')
	driver.maximize_window()

	#Click phone number field
	driver.find_element_by_id('mat-input-0').click() 
	driver.find_element_by_id('mat-input-0').send_keys('9497756047')
	driver.find_element_by_id('mat-input-0').send_keys('\n')

	#Recieves OTP from Mobile
	IPPORT = ("",5002)
	Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	Socket.bind(IPPORT)
	otp=0
	while True:
		data = Socket.recv(1024)
		otp=DisplayNot(data.decode("utf-8"))
		if otp!=0:
			break
		pass
	print(otp)

	#Enter OTP 
	time.sleep(1)
	driver.find_element_by_id('mat-input-1').send_keys(otp)
	driver.find_element_by_id('mat-input-1').send_keys('\n')

	#Clicks on Schecdule Button
	time.sleep(3)
	driver.find_element_by_xpath("//li[@class='bordernone ng-star-inserted']").click()

	#Search via PIN Code 
	time.sleep(3)
	driver.find_element_by_id('mat-input-2').send_keys(pincode)
	driver.find_element_by_id('mat-input-2').send_keys('\n')
	

	#Filter Search
	driver.find_element_by_id('c1').click()
	driver.find_element_by_id('c7').click() 
	driver.find_element_by_id('c3').click() 
	success=0
	#select first option
	try:
		driver.find_element_by_xpath("//a[@class='accessibility-plugin-ac ng-star-inserted']").click()
		success=1
	except:
		notify(title    = pincode,
       	subtitle = 'vaccine not booked',
       	message  = 'All slots filled/Failed to book')
	
	#delay before closing the window
	time.sleep(10)
	driver.close()
    if (success==0):
    	return 0

    return 1


# pincodes = ['670613',
#             '670650',
#             '670642',
#             '670691',
#             '670702',
#             '670692',
#             '673316',
#             '670102',
#             '670643',
#             '670741',
#             '670593',
#             '670007',
#             '670703']

pincodes = ['570023']

date_var = date.today().strftime("%d-%m-%Y")
# sending get request and saving the response as response object
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
flag = 0
success=0
checkVaccine=True
while True:
	success=0
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

        for center in data['centers']:
            for session in center['sessions']:
                if session['available_capacity'] > 0 and session['min_age_limit'] < 45 and session['vaccine'] == 'COVISHIELD':
                    #notify(center['name'],'Vaccine available','Opening Browse')
                    print(center['name'])
                    flag = 1
                    try:
                    	success=bookVaccine(pincode)
                    except:
                    	notify(title    = pincode,
       							subtitle = 'vaccine not booked',
       							message  = 'All slots filled/Failed to book')
                    if success:
                    	checkVaccine=False


        if flag == 0:
            print("Not available at " + str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
