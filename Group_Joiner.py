import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import json
import random
from datetime import date
import calendar
import datetime
from pyautogui import press, typewrite

#URL to check https://www.facebook.com/search/groups/?q=business%20forums

from Config import Config

class Facebook_Group:

    def __init__(self,UserDetails):

        #Get Driver
        driver = self.driver()

        #login
        self.Login(driver,UserDetails)

        #load group file
        f = open('Config/Groups.json')

        # returns JSON object as a dictionary
        data = json.load(f)

        #loop untill i say done
        while True:
            for i in data['Groups']:
                print(i['Name']," - ",i['URL'])
                driver.get(i['URL'])
                time.sleep(10)


            if input("Enter Done, Type Done when moving onto next group") == "Done":
                continue

    def driver(self):

        # Setting Chrome Options
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        # driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options,seleniumwire_options=options)
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)

        return driver

    def Login(self,driver,UserDetails):

        driver.get("https://www.facebook.com/")
        time.sleep(5)

        #Accept Cookies
        driver.find_element("xpath","//button[text()='Only allow essential cookies']").click()
        time.sleep(10)

        #Enter Email
        driver.find_element("xpath","//input[@placeholder='Email address or phone number']").send_keys(UserDetails['Email'])
        time.sleep(2)

        #Enter Password
        driver.find_element("xpath","//input[@placeholder='Password']").send_keys(UserDetails['Password'])
        time.sleep(2)

        #submit
        driver.find_element("xpath","//button[@name='login']").click()
        time.sleep(2)

        #loop untill we input true because it may ask you to
        while True:
            if input("Enter Continue") == "Continue":
                break


while True:
    Facebook_Group(Config.UserDetails)