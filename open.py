from __future__ import print_function
import time
from html.parser import HTMLParser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys
import re
from profanity_check import predict, predict_prob
from bs4 import BeautifulSoup
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import threading 

'''
Awesomeness lent from: https://github.com/dhruvramani/Makeathon-18
'''

driver = webdriver.Firefox(executable_path=r'./Gecko/geckodriver')
driver.get("https://web.whatsapp.com/")
time.sleep(2)
wait = WebDriverWait(driver, 600)
SCOPES = ['https://www.googleapis.com/auth/calendar']

def strip_tags(html):
    return re.sub('<[^<]+?>', '', html)

def search_downloads(file_name):
    while(1):
        if file_name in os.listdir(os.path.join(os.path.expanduser("~"), "Downloads")):
            subject = file_name.split('_')[0]
            if not os.path.exists('{}/Notes/{}'.format(os.path.expanduser('~'), subject)):
                os.mkdir('{}/Notes/{}'.format(os.path.expanduser('~'), subject))
            os.system('mv {}/Downloads/{} {}/Notes/{}/{}'.format(os.path.expanduser('~'), file_name, os.path.expanduser('~'), subject, file_name))
            break

def create_event(event_string, type):
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    if(type==0):
        mesg = event_string.split("\n")
        print(mesg)
        if "tomorrow" in mesg[0].lower():
            start_date = str(datetime.date.today() + datetime.timedelta(days=1))
            end_date = str(datetime.date.today() + datetime.timedelta(days=1))
        elif "today" in mesg[0].lower():
            start_date = str(datetime.date.today())
            end_date = str(datetime.date.today())

        classroom = mesg[1]
        mesg = mesg[2:]

        for line in mesg:
            line = line.split(" ")
            time = line[0]
            course = line[2]

            time = time.split("-")
            if(len(time[0])==2):
                start_time = '{}:00'.format(time[0])
            else:
                start_time = time[0]
            if(len(time[1])==2):
                end_time = '{}:00'.format(time[1])
            else:
                end_time = time[1]

            event = {
              'summary': course,
              'location': classroom,
              'description': course,
              'start': {
                'dateTime': '{}T{}:00+05:30'.format(start_date, start_time),
              },
              'end': {
                'dateTime': '{}T{}:00+05:30'.format(end_date, end_time),
              },
            }

            print(event)
            event = service.events().insert(calendarId='primary', body=event).execute()
            print('Event created: {}'.format(event.get('htmlLink')))
    else:
        mesg = event_string.split("\n")
        print(mesg)
        date_time = mesg[1].split(" ")
        event_loc = mesg[2]
        event_name = mesg[3]

        start_date = date_time[0]
        end_date = date_time[0]

        start_time = date_time[1].split("-")[0]
        end_time = date_time[1].split("-")[1]

        event = {
          'summary': event_name,
          'location': event_loc,
          'description': event_name,
          'start': {
            'dateTime': '{}T{}:00+05:30'.format(start_date, start_time),
          },
          'end': {
            'dateTime': '{}T{}:00+05:30'.format(end_date, end_time),
          },
        }

        print(event)
        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: {}'.format(event.get('htmlLink')))
    # date yyyy-mm-dd, time 24 hrs format


def send_message(target, string):
    #x_arg = '//span[contains(@title,' + target + ')]'
    x_arg = '//span[@title=' + target + ']'
    print(x_arg)
    group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
    print(group_title.get_attribute('innerHTML'))
    group_title.click()
    inp_xpath = '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]'
    input_box = wait.until(EC.presence_of_element_located((By.XPATH, inp_xpath))) 
    print(input_box)
    string = string.replace('\n', Keys.SHIFT + Keys.ENTER + Keys.SHIFT) 
    input_box.send_keys(string + Keys.ENTER)

def mainMessage(sleep=0):
    time.sleep(sleep)
    rightChatBoxes = driver.find_elements_by_css_selector("._2ko65")
    print(rightChatBoxes)

    i = 1
    for rightChatBox in rightChatBoxes:
        soup = BeautifulSoup(rightChatBox.get_attribute('innerHTML'), 'html.parser')
        print(soup.prettify())
        name = soup.select("._19RFN")[0].get('title')
        mesg_time = soup.select("._0LqQ")[0].get_text()
        chatHead = driver.find_elements_by_css_selector(".P6z4j")[0]
        no_messages = int(chatHead.get_attribute('innerHTML'))
        print(no_messages)
        
        rightChatBox.click()

        if i == 1:
            time.sleep(sleep)
            i = i+1

        try :

            messages = driver.find_elements_by_css_selector("._F7Vk")[-no_messages:]   #_2Wx_5 _3LG3B #_12pGw
            print(messages)

            for message in messages:
                mesg = strip_tags(message.get_attribute('innerHTML'))
                print(mesg)
                if ".pdf" in mesg:
                    download_buttons = driver.find_elements_by_css_selector("._1mrMQ")[-no_messages:]   #[0].click()    #_1zGQT oty3x  #_1mrMQ
                    for download_button in download_buttons:
                        if mesg in download_button.get_attribute('innerHTML'):
                            download_button.click()
                            t1 = threading.Thread(target=search_downloads, args=(mesg,)) 
                            t1.start()
                            break

                    #print(download_button)
                else:
                    message.click()
                    mlist = []
                    mlist.append(mesg)
                    is_offensive = predict(mlist)[0]
                    if is_offensive:
                        driver.find_elements_by_css_selector("._2-qoA")[0].click() # 
                        print("click1")
                        driver.find_element(By.XPATH, '//*[@title="Star message"]').click()
                        print("click2")
                        send_message("'Offensive'", "{} @ {} : {}".format(name, mesg_time, mesg))

                    if "timetable" in mesg.lower():
                        create_event(mesg, 0)
                        send_message("'Timetable'", mesg)
                    if "event" in mesg.lower():
                        create_event(mesg, 1)
                
        except Exception as e:
            print(e)
            pass

count = 4
while 1:
    mainMessage(count)
    time.sleep(1)
    count = 0

time.sleep(10)
driver.quit()
