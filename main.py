import sys
import argparse
import helper
import pandas as pd

BASE_PATH = pathlib.Path(__file__).parent.resolve()
WEBDRIVER_FILENAME = "chromedriver" # chrome or firefox
WEBDRIVER_PATH = str(BASE_PATH.joinpath("webdriver/"+WEBDRIVER_FILENAME).resolve())


parser = argparse.ArgumentParser(description='Scrapping Toped Help')
parser.add_argument('--webdriver_path', action='store', type=str, default=WEBDRIVER_PATH,
                    help='chromedriver path ')
parser.add_argument('--product_url', action='store', type=str, default='',
                    help='insert product url ')
parser.add_argument('--get_product', action='store', type=str, default='', 
                    help='get product details ')
parser.add_argument('--get_url', action='store', type=str, default='', 
                    help='get product urls ')
parser.add_argument('--search_key', action='store', type=str, default='',
                    help='Search Keyword')

args = parser.parse_args()

if __name__ == '__main__':
	result = None
	if args.get_url:
		if args.search_key:
    		result = helper.get_product_urls(args.search_key, WEBDRIVER_PATH, option)
    		result.to_csv(str(BASE_PATH.joinpath("-output/product_urls.csv").resolve()), index = False, header=True)
    	else:
    		print("Please also using --search_key 'Keyword'")
    else:
    	if args.product_url:
    		# args.product_url = "https://www.tokopedia.com/36shop/xiaomi-redmi-note-10-pro-6gb-64gb-8gb-128gb-garansi-resmi-xiaomi-bronze-64gb?src=topads"
    		result = helper.get_product_detail(args.product_url, WEBDRIVER_PATH, option)
    		df = pd.DataFrame(result)
    		df.to_csv(str(BASE_PATH.joinpath("-output/product_detail.csv").resolve()), index = False, header=True)
    	else:
    		print("Please also using --product_url 'https://xxxxxxxx'")

    
    print("Scrapping Finished....")

