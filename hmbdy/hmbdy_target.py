from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# set to mweb
opts = Options()
# opts.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_6 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) CriOS/64.0.3282.112 Mobile/15D100 Safari/604.1")
opts.add_argument(" — incognito")

browser = webdriver.Chrome(executable_path='/Library/Application Support/Google/chromedriver', chrome_options=opts)
# '/Users/cbarry/Library/Application Support/Google/chromedriver'

# set up SKU class
class product:
    def __init__(self, sku, name, lead_image, price, review_stars, review_count):
        self.sku = sku
        self.name = name
        self.lead_image = lead_image
        self.price = price
        self.review_stars = review_stars
        self.review_count = review_count

#browser.get("https://github.com/TheDancerCodes")
browser.get("https://www.target.com/s?searchTerm=chairs&sortBy=relevance&Nao=0")

"""# Wait 20 seconds for page to load
timeout = 20
try:
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//img[@class='product-thumb hoverSwap']")))
except TimeoutException:
    print("Timed out waiting for page to load")
    browser.quit()
"""

time.sleep(2)

webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()
for i in range(1, 10):
    browser.execute_script("window.scrollBy(0, 500);")
    time.sleep(3)

# find_elements_by_xpath returns an array of selenium objects.
product_images = browser.find_elements_by_xpath('//div[@data-test="product-image"]/picture[1]/img[1]')
#product_images = browser.find_elements_by_xpath('//a[@data-test="product-image"]')
print(len(product_images))
titles = [x.get_attribute("alt") for x in product_images]
print(titles, '\n')

# use list comprehension to get the actual repo titles and not the selenium objects.
# titles = [x.img.alt for x in titles_element]
# print out all the titles.
#print('titles:')
#print(titles, '\n')


browser.quit()
