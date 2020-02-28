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


driver = webdriver.Firefox(executable_path=r'./Gecko/geckodriver')
driver.get("https://web.whatsapp.com/")
time.sleep(2)
wait = WebDriverWait(driver, 600)

def strip_tags(html):
    return re.sub('<[^<]+?>', '', html)

def create_event(event_string):
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

    # date yyyy-mm-dd, time 24 hrs format
    event = {
          'summary': 'Google I/O 2015',
          'location': '800 Howard St., San Francisco, CA 94103',
          'description': 'A chance to hear more about Google\'s developer products.',
          'start': {
            'dateTime': '{}T{}:00+05:30'.format(start_date, start_time),
          },
          'end': {
            'dateTime': '{}T{}:00+05:30'.format(end_date, end_time),
          },
        }


    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: {}'.format(event.get('htmlLink')))

def send_message(target, string):
    x_arg = '//span[contains(@title,' + target + ')]'
    print(x_arg)
    group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
    print(group_title)
    group_title.click()
    inp_xpath = '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]'
    input_box = wait.until(EC.presence_of_element_located((By.XPATH, inp_xpath))) 
    print(input_box)
    input_box.send_keys(string + Keys.ENTER)

def mainMessage(sleep=0):
    time.sleep(sleep)
    rightChatBoxes = driver.find_elements_by_css_selector("._2ko65")
    print(rightChatBoxes)

    i = 1
    for rightChatBox in rightChatBoxes:
        print(rightChatBox.get_attribute('innerHTML'))
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

            messages = driver.find_elements_by_css_selector("._12pGw")[-no_messages:]
            print(messages)

            for message in messages:
                #star_button = driver.find_elements_by_css_selector("._3zy-4 Sl-9e[value = 'Star message']").click()
                print(star_button)
                mesg = strip_tags(message.get_attribute('innerHTML'))
                print(mesg)
                mlist = []
                mlist.append(mesg)
                is_offensive = predict(mlist)[0]
                if is_offensive:
                    send_message("'Offensive'", "{} @ {} : {}".format(name, mesg_time, mesg))
        except :
            pass

count = 4
while 1:
    mainMessage(count)
    time.sleep(1)
    count = 0

time.sleep(10)
driver.quit()
