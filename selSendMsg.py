from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import sys

driver = webdriver.Firefox()
driver.get("https://web.whatsapp.com/")
wait = WebDriverWait(driver, 600)

target = '"Nabagata Saha"'
string = "Hello sexy"

def web_driver_quit():
	driver.quit()
	quit()

def send_message(target, string):
    x_arg = '//span[contains(@title,' + target.lower() + ')]'
    group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
    group_title.click()
    message = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0]
    message.send_keys(string)
    sendbutton = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/button')[0]
    sendbutton.click()

if __name__ == "__main__":
    send_message(target, string)
    alert1 = driver.SwitchTo().Alert() #remove browser pop-up
    alert1.Accept()
    web_driver_quit()
