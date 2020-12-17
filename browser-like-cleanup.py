#!/usr/bin/env python3

#########################################################################################
# Selenium Script to Log into Twitter, Load the Likes Tab, and Click/Unclick on Likes
# 
# Nick Feamster
# December 18, 2020
#########################################################################################


from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import json
import time

#from selenium.webdriver.firefox.options import Options as FirefoxOptions
#options = FirefoxOptions()
#options.add_argument("--headless")

with open('config.json', 'rt', encoding='utf-8') as data_file:
    json_data = data_file.read()
credentials = json.loads(json_data)[0]

user = credentials['user']
password = credentials['password']


def site_login(driver):
    driver.get("https://twitter.com/login")
    driver.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div[1]/form/div/div[1]/label/div/div[2]/div/input').send_keys(user)
    driver.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div[1]/form/div/div[2]/label/div/div[2]/div/input').send_keys(password)
    driver.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div[1]/form/div/div[3]/div/div/span/span').click()

def get_likes(driver):

    driver.get("https://twitter.com/feamster/likes")
    driver.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/nav/div/div[2]/div/div[4]/a/div/span').click()

    while True:
            id_str = "//div[@data-testid='like']"

            # Note: This Clicks and then Unclicks due to a Bug in the Twitter API
            # If doing this simply to unlike, remove the second click.
            like_elem = driver.find_element_by_xpath(id_str)
            like_elem.click()
            time.sleep(1)

            # Second Click: Possibly optional if you're manually unliking.
            like_elem.click()

            # Refresh the page so that the liked post is deleted and the next one to delete is at top.
            driver.refresh()
            time.sleep(5)


#################

driver = webdriver.Firefox()
site_login(driver)
get_likes(driver)
