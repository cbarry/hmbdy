from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

option = webdriver.ChromeOptions()
option.add_argument(" — incognito")

browser = webdriver.Chrome(executable_path='/Users/cbarry/Library/Application Support/Google/chromedriver', chrome_options=option)
# '/Users/cbarry/Library/Application Support/Google/chromedriver'

#browser.get("https://github.com/TheDancerCodes")
browser.get("https://www.westelm.com/shop/furniture/sectionals")

"""# Wait 20 seconds for page to load
timeout = 20
try:
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//img[@class='product-thumb hoverSwap']")))
except TimeoutException:
    print("Timed out waiting for page to load")
    browser.quit()
"""

time.sleep(5)

modal = browser.find_element_by_class_name("stickyOverlayMinimizeButton").click()
# modal.send_keys(Keys.ESCAPE).perform()

# find_elements_by_xpath returns an array of selenium objects.
titles_element = browser.find_elements_by_xpath("//a[@class='product-name']")
# use list comprehension to get the actual repo titles and not the selenium objects.
titles = [x.text for x in titles_element]
# print out all the titles.
print('titles:')
print(titles, '\n')
