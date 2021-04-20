import sys
import argparse
import pathlib
import helper
import pandas as pd
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BASE_PATH = pathlib.Path(__file__).parent.resolve()
WEBDRIVER_FILENAME = "chromedriver" # chrome or firefox
WEBDRIVER_PATH = str(BASE_PATH.joinpath("webdriver/"+WEBDRIVER_FILENAME).resolve())

#argument for incognito Chrome
option = Options()
# option.add_argument('--user-data-dir=./User_Data')
option.add_argument("--incognito")


parser = argparse.ArgumentParser(description='Scrapping Toped Help')
parser.add_argument('--webdriver_path', action='store', type=str, default=WEBDRIVER_PATH,
                    help='chromedriver path ')

parser.add_argument('--mode', action='store', type=str, default='url', # product 
                    help='get urls or product details ')

## collect product information detail

parser.add_argument('--product_url', action='store', type=str, default='',
                    help='insert product url ')
parser.add_argument('--use_csv', action='store', type=str, 
                    default=str(BASE_PATH.joinpath("_output/product_urls.csv").resolve()),help='insert csv file path that contains product detail ')
parser.add_argument('--search_key', action='store', type=str, default='',
                    help='Search Keyword')
parser.add_argument('--limit_pages', action='store', type=str, default='',
                    help='Page limitation')

args = parser.parse_args()

if __name__ == "__main__":
    
    if args.mode == 'url':
        if args.search_key:
            result = helper.get_product_urls(args.search_key ,WEBDRIVER_PATH, option,  args.limit_pages)
            path_csv = str(BASE_PATH.joinpath("_output/product_urls.csv").resolve())

            df = pd.DataFrame(result)
            print(df['url'][0])
            df.to_csv(path_csv, index = False, header=True)
            print("Output path ",str(BASE_PATH.joinpath("_output/product_urls.csv").resolve()))
        else:
            print("Please also using --search_key 'Keyword'")
    else:
        if args.product_url:
            # args.product_url = "https://www.tokopedia.com/36shop/xiaomi-redmi-note-10-pro-6gb-64gb-8gb-128gb-garansi-resmi-xiaomi-bronze-64gb?src=topads"
            print("One Product Url")
            result = helper.get_product_detail(args.product_url, WEBDRIVER_PATH, option)
            df = pd.DataFrame(result)
            df.to_csv(path_csv, index = False, header=True)
        else:
            print("Many Product Urls")
            path_csv = str(BASE_PATH.joinpath("_output/product_details.csv").resolve())
            try:
                failed = 0
                df = pd.DataFrame()
                df_urls = pd.read_csv(args.use_csv)
                for value_url in list(df_urls["url"]):
                    try:
                        result = helper.get_product_detail(value_url, WEBDRIVER_PATH, option)
                    except:
                        print("Link Gagal: ", value_url)
                        raise
                    df_result = pd.DataFrame(result)
                    df = pd.concat([df, df_result])
                df.reset_index(inplace=True)
                df.to_csv(path_csv, index = True, header=True)
                print("Output path ",path_csv)
            except:
                raise            

    
    print("Scrapping Finished....")

