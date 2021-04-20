import os
import sys
import pathlib
import urllib
import re
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import reversed_humanize

# BASE_PATH = pathlib.Path(__file__).parent.resolve()
# WEBDRIVER_FILENAME = "chromedriver" # chrome or firefox
# WEBDRIVER_PATH = str(BASE_PATH.joinpath("webdriver/"+WEBDRIVER_FILENAME).resolve())
RESOLUTION_HEIGHT = 700
SCROLL_PAUSE_TIME = 10
# Wait 20 seconds for page to load
TIMEOUT = 20


#argument for incognito Chrome
option = Options()
# option.add_argument('--user-data-dir=./User_Data')
option.add_argument("--incognito")



def get_product_detail(product_url,chrome_path, chrome_options):

    browser = webdriver.Chrome(executable_path=chrome_path,  options=chrome_options)
    browser.get(product_url)
    # Pada pengiriman tidak terload, sehingga perlu dua kali
    browser.get(product_url)

    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")

    scroll = RESOLUTION_HEIGHT
    while last_height//scroll > 0:
        # Scroll down to bottom per hight of resolution
        browser.execute_script("window.scrollTo(0, %s)" % (scroll))
        scroll += RESOLUTION_HEIGHT

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

    try:
        WebDriverWait(browser, TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='css-856ghu']")))
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()

    soup = BeautifulSoup(browser.page_source, "html.parser")
    name = soup.find_all('h1', class_='css-v7vvdw')[0].get_text()
    price = soup.find_all('div', class_='price')[0].get_text()
    ringkasan = soup.find_all('div', class_='items')[0].get_text().split('•')

    terjual_int = 0
    rating_int = 0
    ulasan_int = 0
    ulasan_terbaru = None
    waktu_ulasan_tanggal = None
    waktu_diskusi_tanggal = None
    waktu_balasan_tanggal = None
    text_balasan_terbaru = None

    for ringkasan_text in ringkasan:
        if "terjual" in ringkasan_text.lower():
            terjual = ringkasan_text
            terjual_int = int(terjual.replace("Terjual ",""))
        elif "ulasan" in ringkasan_text:
            rating_count = ringkasan_text
            _, rating_int, ulasan_count,_ = rating_count.split(" ")
            ulasan_int = ulasan_count.replace("(","")

            ulasan = soup.find( id='pdp_comp-review')
            baris_ulasan = ulasan.find_all('div', class_='css-e8n84a')
            ulasan_terbaru =baris_ulasan[0].find_all('p', class_='css-1np3d84-unf-heading e1qvo2ff8')[0].get_text()
            waktu_ulasan = baris_ulasan[0].find_all('p', class_='css-oals0c-unf-heading e1qvo2ff8')[0].get_text()
            waktu_ulasan_tanggal = reversed_humanize.humanize_to_date(waktu_ulasan)
        elif "diskusi" in ringkasan_text.lower():
            diskusi_count  = ringkasan_text
            diskusi = soup.find_all('ul', class_='css-1vr8bhw')
            if diskusi:
                diskusi_terbaru = diskusi[0].find_all('li')[0]
                waktu_diskusi = diskusi_terbaru.find_all('span', class_ ='css-olhslp')[0].get_text()
                waktu_diskusi_tanggal = reversed_humanize.humanize_to_date(waktu_diskusi)
                balasan = diskusi_terbaru.find_all('ul', class_='css-4dtaj')
                balasan_terbaru = balasan[0].findAll('li')[-1]
                waktu_balasan = balasan_terbaru.find_all('span', class_ ='css-olhslp')[0].get_text()
                waktu_balasan_tanggal = reversed_humanize.humanize_to_date(waktu_balasan)
                text_balasan_terbaru = balasan_terbaru.find_all('p', class_ ='css-13bzwm2')[0].get_text()

    detail = soup.find_all('ul', class_='css-1ijyj3z e1iszlzh2')
    details = [li.get_text() for li in detail[0].findAll('li')]    
    kondisi, berat, kategori, etalase = details
    kondisi = kondisi.split(":")[1].strip()
    pengiriman = soup.find_all('div', class_='css-1dxest3')
    asal = pengiriman[0].find_all('div', class_='css-1wx7lrk pad-bottom')[0].get_text()
    asal = asal.replace("Dikirim dari","")
    price_int = int(price.replace("Rp","").replace(".",""))
    berat_int = berat.split(" ")[1].strip()

    browser.quit()
    product_detail = [
                        ("nama produk", [name]),
                        ("harga", [price_int]),
                        ("jumlah terjual",[terjual_int]),
                        ("kondisi ", [kondisi]),
                        ("berat ", [berat_int]),
                        ("rating ", [rating_int]),
                        ("jumlah ulasan", [ulasan_int]),
                        ("asal pengiriman", [asal]),
                        ("ulasan terbaru", [ulasan_terbaru]),
                        ("waktu ulasan terbaru", [waktu_ulasan_tanggal]),
                        ("waktu diskusi terbaru", [waktu_diskusi_tanggal]),
                        ("waktu balasan terbaru",[waktu_balasan_tanggal]),
                        ("balasan diskusi terbaru", [text_balasan_terbaru])
                    ]
    return dict(product_detail)


def get_product_urls(keyword_str,chrome_path, chrome_options, limit_pages=None):

    keyword = urllib.parse.quote(keyword_str)

    browser = webdriver.Chrome(executable_path=chrome_path,  options=chrome_options)

    product_urls = {'name':[], 'url':[]}
    
    page = pages = 1
    while pages >= page :
        if page:
            browser.get("https://www.tokopedia.com/search?st=product&q="+keyword+"&page="+str(page))
        else:
            browser.get("https://www.tokopedia.com/search?st=product&q="+keyword)

        # Get scroll height
        last_height = browser.execute_script("return document.body.scrollHeight")
        scroll = RESOLUTION_HEIGHT
        while last_height//scroll > 0:
            # Scroll down to bottom per hight of resolution
            browser.execute_script("window.scrollTo(0, %s)" % (scroll))
            scroll += RESOLUTION_HEIGHT

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)


        try:
            elements = WebDriverWait(browser, TIMEOUT).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='css-7fmtuv']//a")))
            name_elements = WebDriverWait(browser, TIMEOUT).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='css-18c4yhp']")))
        except TimeoutException:
            print("Timed out waiting for page to load")
            browser.quit()

        for name_element, element in zip(name_elements,elements):
            product_name = name_element.text

            #get href
            split_point = "https%3A%2F%2Fwww.tokopedia.com"
            href = element.get_attribute('href')
            if split_point in href:
                href = urllib.parse.unquote(split_point+str(re.split(r"https%3A%2F%2Fwww.tokopedia.com", href)[-1]))
                href = re.split(r"&", href)[0]

            
            product_urls['name'].append(product_name)
            product_urls['url'].append(str(href))

        if page == 1:
            pages_elements = WebDriverWait(browser, TIMEOUT).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"button.css-13ld6kr-unf-pagination-item.e19tp72t1")))
            if limit_pages:
                pages = int(limit_pages)
            else:
                pages = int(str(pages_elements[-1].text).replace('.',''))
        page+=1

    # df = pd.DataFrame(product_urls)

    browser.quit()
    return product_urls

    try:
        pass
    except Exception as e:
        raise
    else:
        pass
    finally:
        pass



