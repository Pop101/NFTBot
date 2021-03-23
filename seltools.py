import time

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.common.exceptions import NoSuchElementException 

def wait_for_element_pass(driver, xpath='//*[@class="progress"]', timeout = 30):
    """Waits for an element to appear, then disappear. Default case: Progress bar"""
    t = time.time()
    while True: # Shitty do while loop
        element = wait_for_element(driver, xpath, timeout=timeout/2)
        WebDriverWait(driver, timeout/2).until(staleness_of(element))
        time.sleep(0.1)
        if len(driver.find_elements_by_xpath(xpath)) == 0:
            break
        if time.time() > t + timeout:
            break

def wait_for_element(driver, xpath, timeout = 30):
    return WebDriverWait(driver, timeout).until(presence_of_element_located((By.XPATH, xpath)))

def wait_for_page_load(driver, timeout=30):
    old_page = driver.find_element_by_tag_name('html')
    yield WebDriverWait(driver, timeout).until(staleness_of(old_page))

def safeclick(driver, element):
    loc = element.rect
    print(loc)
    eloc = driver.execute_script(
        "return document.elementFromPoint(arguments[0], arguments[1]);",
        loc['x']+5,
        loc['y']+5
    )
    if eloc != None: eloc.click()
    else:
        try: element.click()
        except: element.find_element_by_xpath('./..').click()

def submit(driver):
    """Presses any 'submit' button"""
    safeclick(driver, wait_for_element(driver, '//*[@type="submit"]'))