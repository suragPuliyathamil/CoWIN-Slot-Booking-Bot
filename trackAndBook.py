"""
MIT License

Copyright (c) 2021 Surag Puliyathamil

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation 
files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, 
modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software 
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE 
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR 
IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
import time
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import socket
import requests
import os

def coverter(text):
    #get otp from entire message in utf-8
    data=text.decode("utf-8")
    data = data.split(" ")
    if len(data)>6 :
        return data[6][:-1]
    return 0

def notify(title, subtitle, message):
    #send notification
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    os.system('terminal-notifier {}'.format(' '.join([m, t, s])))
        
def trackVaccine(pincode):
    URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode="+pincode+"&date="+date.today().strftime("%d-%m-%Y")
    r = requests.get(url=URL)
    data = r.json()
    checkVaccine=True
    try:
        while checkVaccine:
            time.sleep(4)
            for center in data['centers']:
                for session in center['sessions']:
                    if  checkVaccine:
                        if session['available_capacity_dose1'] > 0 :
                        #Uncomment the below line and comment the above line to change from dose 1 to dose 2
                        #if session['available_capacity_dose1'] > 0 :
                            if session['min_age_limit'] == 18:
                                if  session['vaccine'] == 'COVISHIELD':
                                    print(center['name'])
                                    return 1
                                
    except:
        return 0

def bookVaccine(pincode):
    
    #open URL
    url='https://selfregistration.cowin.gov.in'
    driver=openurl(url)
    
    #Set Number and get OTP
    driver=getOTP(driver,'9497756047')

    #Clicks on Schecdule Button
    driver.find_element_by_xpath("//li[@class='bordernone ng-star-inserted']").click()
    time.sleep(3)

    #Search via PIN Code 
    driver=setPincode(driver, pincode)
    
    #Filter Search
    driver=applyFilter(driver)
    
    try:
        #book the first available slot in the first entry
        driver=findAndBookslot(driver, pincode)
    except:
        #return Notification 
        print("failed to book vaccine")
        notify(title    = pincode,subtitle = 'vaccine not booked',message  = 'All slots filled/Failed to book')
        
    #close the window
    time.sleep(3)
    driver.close()

def openurl(url):
    #open url in chrome driver
    driver = webdriver.Chrome('/Users/surag/Desktop/CowinBot/chromedriver')
    driver.get(url)
    driver.maximize_window()
    return driver

def getOTP(driver,number):
    #Enter Number and Get OTP on mobile
    driver.find_element_by_id('mat-input-0').click() 
    driver.find_element_by_id('mat-input-0').send_keys(number)
    driver.find_element_by_id('mat-input-0').send_keys('\n')
    
    #Setup For Localhost to obtain OTP
    IPPORT = ("",5002)
    Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    Socket.bind(IPPORT)
    otp=0
    while True:
        data = Socket.recv(1024)
        otp=coverter(data)
        if otp!=0:
            break
        pass
    print(otp)

    #Entering OTP 
    driver.find_element_by_id('mat-input-1').send_keys(otp)
    driver.find_element_by_id('mat-input-1').send_keys('\n')
    time.sleep(4)
    return driver
  
def applyFilter(driver):
    driver.find_element_by_id('c1').click()        #age 18+
    #driver.find_element_by_id('c1').click()       #age 45+
    driver.find_element_by_id('c6').click()        #paid 
    driver.find_element_by_id('c7').click()        #unpaid
    driver.find_element_by_id('c3').click()        #covishield 
    return driver

def setPincode(driver,pincode):
    driver.find_element_by_id('mat-input-2').send_keys(pincode)
    driver.find_element_by_id('mat-input-2').send_keys('\n')
    time.sleep(2)
    return driver

def findAndBookslot(driver,pincode):
    #click on First Covishield Button
    time.sleep(1)
    driver.find_element_by_xpath("//a[@class='accessibility-plugin-ac ng-star-inserted']").click() 
    
    #click on the first available time slot 
    time.sleep(3)
    driver.find_element_by_xpath("//ion-button[@type='submit']").click()
    
    #click on cofirm
    time.sleep(2)
    driver.find_element_by_xpath("//button[@aria-label='Confirm']").click() 
    notify(title    = pincode,subtitle = 'vaccine booked',message  = 'Booked Succesfully')
    return driver
    
    
pincode = '570023'
vaccineAvailable=trackVaccine(pincode)
if vaccineAvailable :
    try:
        bookVaccine(pincode)
        
    except:
        notify(pincode,'vaccine not booked','All slots filled/Failed to book')
