import time
from nltkrun import classify
from html.parser import HTMLParser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys
import re
from profanity_check import predict, predict_prob



driver = webdriver.Firefox(executable_path=r'./Gecko/geckodriver')
driver.get("https://web.whatsapp.com/")
time.sleep(2)
wait = WebDriverWait(driver, 600)

def strip_tags(html):
    return re.sub('<[^<]+?>', '', html)

'''def send_message(target, string):
    x_arg = '//span[contains(@title,' + target.lower() + ')]'
    group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
    group_title.click()
    message = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0]
    message.send_keys(string)
    sendbutton = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/button')[0]
    sendbutton.click()'''

def send_message(target, string):
    x_arg = '//span[contains(@title,' + target + ')]'
    print(x_arg)
    group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
    print(group_title)
    group_title.click()
    #message = driver.find_element(By.XPATH , '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]') #find_elements_by_xpath('//*[@id="main"]/footer/div[0]/div[1]/div[0]/div[1]')[0]
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
        chatHead = driver.find_elements_by_css_selector(".P6z4j")[0]
        #print(chatHead)
        no_messages = int(chatHead.get_attribute('innerHTML'))
        print(no_messages)

        rightChatBox.click()

        if i == 1:
            time.sleep(sleep)
            i = i+1

        try :

            messages = driver.find_elements_by_css_selector("._12pGw")[-no_messages:]

            for message in messages:
                mess = strip_tags(message.get_attribute('innerHTML'))
                mlist = []
                mlist.append(mess)
                is_offensive = predict(mlist)[0]
                if is_offensive:
                    send_message("'Offensive'", mess)
                '''group_name = "'" + classify(mess)[0] + "'"
                print(mess)
                print(group_name)

                send_message(group_name, mess)'''
        except :
            pass
#            alert1 = driver.SwitchTo().Alert()
#            alert1.Accept()



count = 4
while 1:
    mainMessage(count)
    time.sleep(1)
    count = 0

time.sleep(10)
driver.quit()
