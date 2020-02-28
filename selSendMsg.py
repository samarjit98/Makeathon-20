from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import sys

driver = webdriver.Firefox(executable_path=r'./Gecko/geckodriver')
driver.get("https://web.whatsapp.com/")
wait = WebDriverWait(driver, 600)

target = '"Aise hi"'
string = "Hello sexy"

def web_driver_quit():
	driver.quit()
	quit()

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
    #sendbutton = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/button')[0]
    #print(sendbutton)
    #sendbutton.click() 

if __name__ == "__main__":
    send_message(target, string)
    alert1 = driver.SwitchTo().Alert() #remove browser pop-up
    alert1.Accept()
    web_driver_quit()
