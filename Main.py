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

class Facebook_Group:

    def __init__(self,UserDetails):

        if UserDetails["Active"] == "True":
            print("In page",UserDetails)

            #Get Driver
            driver = self.driver()

            #login
            self.Login(driver,UserDetails)

            # Set start and end times
            start = datetime.time(10, 00, 0)
            end = datetime.time(9, 00, 0)

            while True:
                #Create the week First
                week = self.CreateWeek()

                # loop days in the week
                End = 0
                while End != 1:

                    # Get todays date and time
                    my_date = date.today()
                    current = datetime.datetime.now().time()

                    End = 1
                    for i in week['Days']:

                        # If todays date then print today and not already done
                        if i['Day'] == calendar.day_name[my_date.weekday()] and i['DoneDay'] == 0 and self.time_in_range(start, end,current) is True:

                            for Group in i["Groups"]:
                                print(Group)
                                try:
                                    self.LoadPage(Group["URL"], driver,UserDetails)
                                except Exception as E:
                                    print(E)
                            i['DoneDay'] = 1
                            End = 0
                            print("Going to sleep for the day",i)
                            time.sleep(random.randint(86400, 88400))
                            break

                    print("sleep")
                    time.sleep(random.randint(1900, 3600))

        else:
            return

    def CreateWeek(self):
        # Opening JSON file
        import time

        f = open('Config/Groups.json')

        # returns JSON object as a dictionary
        data = json.load(f)

        # how many a groups day and set days
        DayGroup = int(((len(data['Groups']) + 2) / 7))
        print("Groups Per Day", DayGroup)

        # Set default values
        DaysList = {"Days": [
            {
                "Day": "Monday",
                "DoneDay": 0,
                "Amount": 0,
                "PostAmount": random.randint((DayGroup - 1), (DayGroup + 1)),
                "Groups": [
                ]
            },
            {
                "Day": "Tuesday",
                "DoneDay": 0,
                "Amount": 0,
                "PostAmount": random.randint((DayGroup - 1), (DayGroup + 1)),
                "Groups": [
                ]
            },
            {
                "Day": "Wednesday",
                "DoneDay": 0,
                "Amount": 0,
                "PostAmount": random.randint((DayGroup - 1), (DayGroup + 1)),
                "Groups": [
                ]
            },
            {
                "Day": "Thursday",
                "DoneDay": 0,
                "Amount": 0,
                "PostAmount": random.randint((DayGroup - 1), (DayGroup + 1)),
                "Groups": [
                ]
            },
            {
                "Day": "Friday",
                "DoneDay": 0,
                "Amount": 0,
                "PostAmount": random.randint((DayGroup - 1), (DayGroup + 1)),
                "Groups": [
                ]
            },
            {
                "Day": "Saturday",
                "DoneDay": 0,
                "Amount": 0,
                "PostAmount": random.randint((DayGroup - 1), (DayGroup + 1)),
                "Groups": [
                ]
            },
            {
                "Day": "Sunday",
                "DoneDay": 0,
                "Amount": 0,
                "PostAmount": random.randint((DayGroup - 1), (DayGroup + 1)),
                "Groups": [
                ]
            }
        ]
        }

        # loop the groups and add them into the DaysList, first loop looks for groups with set days
        End = 0
        loop = 0
        while End == 0:

            # if looped 25 times then quit
            if loop < 25:
                loop += 1
            else:
                End = 1
                break

            for i in data['Groups']:

                # Check to make sure there is still groups to be added
                End = 1
                for check in data['Groups']:
                    # if buisness and done 0 then list is not done carry on
                    if check["Done"] == 0 and check["Type"] == 'Business':
                        End = 0

                    # if post not Any, add to group and remove
                    if check["Done"] == 0 and check["Type"] == 'Business' and check['PostDates'] != "Any":

                        for b in DaysList['Days']:
                            if check['PostDates'] == b['Day'] and b['PostAmount'] != 0:
                                # append group to post days
                                b['Groups'].append(check)
                                # take one of post ammount
                                b['Amount'] = b['Amount'] + 1
                                # take one of post ammount
                                b['PostAmount'] = b['PostAmount'] - 1
                                # Mark as done
                                check['Done'] = 1
                                break

                if End == 1:
                    break

                # if post is any
                if random.randint(1, 2) == 1 and i['PostDates'] == "Any" and i['Done'] == 0 and i['Type'] == "Business":
                    for b in DaysList['Days']:
                        if b['PostAmount'] != 0:
                            # append group to post days
                            b['Groups'].append(i)
                            # take one of post ammount
                            b['Amount'] = b['Amount'] + 1
                            # take one of post ammount
                            b['PostAmount'] = b['PostAmount'] - 1
                            # Mark as done
                            i['Done'] = 1
                            break

        # Closing file
        f.close()

        for b in DaysList['Days']:
            print(b)

        return DaysList


    def driver(self):

        # Setting Chrome Options
        #chrome_options = Options()
        # chrome_options.add_argument("--headless")
        # driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options,seleniumwire_options=options)
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())

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
            print("Go to ",UserDetails['Name'])
            if input("Enter Continue") == "Continue":
                break

        driver.get(UserDetails["FBPage"])
        time.sleep(5)

        #loop untill we input true because it may ask you to
        while True:
            print("Go to ",UserDetails['Name'])
            if input("Enter Continue") == "Continue":
                break

    def time_in_range(self,start, end, current):
        """Returns whether current is in the range [start, end]"""
        return start <= current <= end

    def LoadPage(self,URL,driver,UserDetails):

        driver.get(URL)
        time.sleep(random.randint(5, 10))

        #Click Write Something
        try:
            driver.find_element("xpath","//span[text()='Write something...']").click()
            time.sleep(random.randint(5, 10))
        except Exception as E:
            print(E)

        #enter text
        elem = driver.switch_to.active_element
        Text = UserDetails['Text']
        elem.send_keys(random.choice(Text))
        time.sleep(random.randint(5, 10))

        #Click Post
        elem = driver.switch_to.active_element
        elem.find_element("xpath","//span[text()='Post']").click()
        time.sleep(random.randint(5, 10))

        time.sleep(random.randint(10, 60))