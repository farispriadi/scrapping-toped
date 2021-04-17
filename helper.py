import os
import sys
import pathlib
import argparse
import urllib
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

BASE_PATH = pathlib.Path(__file__).parent.resolve()
WEBDRIVER_FILENAME = "chromedriver" # chrome or firefox
WEBDRIVER_PATH = str(BASE_PATH.joinpath("webdriver/"+WEBDRIVER_FILENAME).resolve())

#argument for incognito Chrome
option = Options()
option.add_argument('--user-data-dir=./User_Data')
option.add_argument("--incognito")

parser = argparse.ArgumentParser(description='Scrapping Toped Help')
parser.add_argument('--webdriver_path', action='store', type=str, default=WEBDRIVER_PATH,
                    help='chromedriver path ')
parser.add_argument('--search_key', action='store', type=str, default='',
                    help='Search Keyword')

args = parser.parse_args()



# soup = BeautifulSoup(browser.page_source, "html.parser")

# product_items = soup.find_all("div", attrs={"data-qa-locator": "product-item"})
# for item in product_items:
#     item_url = f"https:{item.find('a')['href']}"
#     print(item_url)

#     browser.get(item_url)

#     item_soup = BeautifulSoup(browser.page_source, "html.parser")

#     # Use the item_soup to find details about the item from its url.

def get_product_links(keyword_str ,chrome_path, chrome_options):

    keyword = urllib.parse.quote(keyword_str)

    browser = webdriver.Chrome(executable_path=chrome_path,  options=chrome_options)

    product_urls = {'name':[], 'url':[]}
    
    page = pages = 1
    while pages >= page :
        if page:
            browser.get("https://www.tokopedia.com/search?st=product&q="+keyword+"&page="+str(page))
        else:
            browser.get("https://www.tokopedia.com/search?st=product&q="+keyword)

        # Wait 20 seconds for page to load
        timeout = 20

        SCROLL_PAUSE_TIME = 5

        # Get scroll height
        last_height = browser.execute_script("return document.body.scrollHeight")

        print("last_height",last_height)
        scroll = 768
        while last_height//scroll > 0:
            # Scroll down to bottom per hight of resolution
            browser.execute_script("window.scrollTo(0, %s)" % (scroll))
            scroll += 768

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)


        try:
            elements = WebDriverWait(browser, timeout).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='css-7fmtuv']//a")))
            name_elements = WebDriverWait(browser, timeout).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='css-18c4yhp']")))
        except TimeoutException:
            print("Timed out waiting for page to load")
            browser.quit()

        for name_element, element in zip(name_elements,elements):
            product_name = name_element.text

            #get href
            href = element.get_attribute('href')
            
            product_urls['name'].append(product_name)
            product_urls['url'].append(href)

        if page == 1:
            pages_elements = WebDriverWait(browser, timeout).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"button.css-13ld6kr-unf-pagination-item.e19tp72t1")))
            print("last_page ",pages_elements[-1].text)        
            pages = int(str(pages_elements[-1].text).replace('.',''))
        page+=1

    df = pd.DataFrame(product_urls)

    browser.quit()
    return df


if __name__ == '__main__':

    result = get_product_links(args.search_key, WEBDRIVER_PATH, option)
    print("result",result)
    
    print("Scrapping Finished....")
