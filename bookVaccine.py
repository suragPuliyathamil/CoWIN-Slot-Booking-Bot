import time
from datetime import date
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from PyQt5 import Qt
import sys
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
        notify(title    = pincode,subtitle = 'vaccine not booked',message  = 'All slots filled/Failed to book')
        
    #close the window
    time.sleep(3)
    driver.close()
    return 1

bookVaccine('670613')