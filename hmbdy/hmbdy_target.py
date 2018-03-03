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

# set up product class
class product:
    def __init__(self, sku, name, lead_image, price, review_stars, review_count):
        self.sku = sku or ''
        self.name = name or ''
        self.lead_image = lead_image or ''
        self.price = price or ''
        self.review_stars = review_stars or ''
        self.review_count = review_count or ''

def get_product_info(product_page):
    product_facts = browser.find_elements_by_xpath('//*[@id="tabContent-tab-details"]/div/div[1]/')
    print(len(product_facts))
    #first div is always product description
    description = product_facts[0].text

def get_product_image(product_page):
    pass

productList = []

#browser.get("https://github.com/TheDancerCodes")
browser.get("https://www.target.com/s?searchTerm=chairs&sortBy=relevance&Nao=0&limit=96")

time.sleep(1)

webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()
for i in range(1, 35):
    browser.execute_script("window.scrollBy(0, 500);")
    time.sleep(1)

# find_elements_by_xpath returns an array of selenium objects.
product_cards = browser.find_elements_by_xpath('//div[@data-test="product-card"]/div[1]/h3[1]/a[1]')
print(len(product_cards))

links = [x.get_attribute("href") for x in product_cards]
print(links, '\n')

for link in links:
    prod_page = browser.get(link)
    for i in range(1, 8):
        browser.execute_script("window.scrollBy(0, 500);")
        time.sleep(1)
    get_product_info(prod_page)
    break

# use list comprehension to get the actual repo titles and not the selenium objects.
# titles = [x.img.alt for x in titles_element]
# print out all the titles.
#print('titles:')
#print(titles, '\n')


browser.quit()
