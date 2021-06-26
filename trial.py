from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
from PyQt5 import Qt
import sys
import socket

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

# notify(title    = 'Aster MIMS',
#        subtitle = 'vaccine',
#        message  = 'Opening webbrowser')

#Open Chrome Driver in full window
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
driver.find_element_by_id('mat-input-2').send_keys('570001')
time.sleep(1)
driver.find_element_by_id('mat-input-2').send_keys('\n')

#Filter Search
driver.find_element_by_id('c1').click()
driver.find_element_by_id('c7').click() 
driver.find_element_by_id('c3').click() 

#select first option
try:
	driver.find_element_by_xpath("//a[@class='accessibility-plugin-ac ng-star-inserted']").click()
except:
	notify(title    = 'Aster MIMS',
       subtitle = 'NO available vaccine',
       message  = 'All slots filled')


