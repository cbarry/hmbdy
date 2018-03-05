from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

import time
import json
import re
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


# set to mweb
opts = Options()
# opts.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_6 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) CriOS/64.0.3282.112 Mobile/15D100 Safari/604.1")
opts.add_argument(" — incognito")

browser = webdriver.Chrome(executable_path='/Library/Application Support/Google/chromedriver', chrome_options=opts)
browser.set_script_timeout(15)

# scrape the products on a given PLP
def scrape_PLP(base_url):
    pdp_links = {}
    browser.get(base_url)
    time.sleep(1)

    webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()
    for i in range(1, 10):
        browser.execute_script("window.scrollBy(0, 500);")
        time.sleep(1)

    product_cards = browser.find_elements_by_xpath('//div[@data-test="product-card"]/div[1]/h3[1]/a[1]')
    print(len(product_cards))

    pdp_links = [x.get_attribute("href") for x in product_cards]
    print(pdp_links, '\n')

    # scrape every PDP on this page
    product_infos = []
    for link in pdp_links:
        prod_page = browser.get(link)
        webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()
        for i in range(1, 1):
            browser.execute_script("window.scrollBy(0, 500);")
            time.sleep(1)
        try:
            browser.find_element_by_xpath('//*[@id="tabContent-tab-details"]/div/div[3]/button').click()
        except:
            # this is a broken product next_page
            product_infos.append({'product_url': link, 'scrape_successful': 'false'})
        else:
            product_infos.append(get_product_info(prod_page))

    return product_infos

# scrape the product info on a given PDP
def get_product_info(product_page):
    product_facts = {}
    # get product name
    name = browser.find_element_by_xpath('//*[@id="mainContainer"]/div/div/div[1]/div/div[1]/h1/span').text
    product_facts["product_name"] = name

    # get product URL
    product_facts["product_url"] = browser.current_url

    # get product SKU
    product_facts["SKU"] = re.search('(?<=\/A-)\d{2,15}', browser.current_url).group(0)

    # get product lead image URL — this is not so smart
    #image_url = browser.find_element_by_xpath('//div[@class="slide--active"]/a[1]/div[1]/div[1]/picture/img').get_attribute('src')
    product_facts["product_lead_image"] = 'http://target.scene7.com/is/image/Target/' + product_facts["SKU"] + '?wid=488&hei=488&fmt=pjpeg'

    # get product price
    price = browser.find_element_by_xpath('//div[@data-test="product-price"]/span').text

    # get rating count
    product_facts["rating_count"] = browser.find_element_by_xpath('//span[@data-test="ratingCount"]/span').text

    # get average rating
    rating_length = browser.find_element_by_xpath('//div[@data-ref="rating-mask"]').get_attribute('style')
    try:
        product_facts["average_rating"] = re.search('(?<=width: )\d{1,3}', rating_length).group(0)
    except:
        product_facts["average_rating"] = '0'

    # get product description
    product_fact_div = browser.find_elements_by_xpath('//*[@id="tabContent-tab-details"]/div/div[1]/*')
    #first div is always product description
    product_facts["description"] = product_fact_div[0].text
    for i in range(len(product_fact_div)-1):
        fact_text = product_fact_div[i+1].text
        try:
            product_facts[fact_text.split(":", 1)[0]] = fact_text.split(":", 1)[1].lstrip()
        except:
            break
    print(product_facts)
    return product_facts

# start here
product_infos = []
#base_url = "https://www.target.com/c/chairs-living-room-furniture/-/N-5xtlz?limit=96&Nao=0"
base_url = "https://www.target.com/c/chairs-living-room-furniture/-/N-5xtlz?limit=5&Nao=0"
file_path = '/tmp/hmbdy_temp_' + time.strftime("%d-%b-%Y %H.%M.%S") + '.txt'

next_page = True
while next_page :
    product_infos.append(scrape_PLP(base_url))
    print(product_infos)

    with open(file_path, 'a') as file:
        file.write(json.dumps(product_infos))

    # Try to find the next PLP page and go to it
    try:
        browser.get(base_url)
        base_url = browser.find_element_by_xpath('//a[@data-test="next"]').get_attribute("href")
        print(base_url)
    except:
        print("no next page")
        next_page = False

browser.quit()
