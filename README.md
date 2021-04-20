# Scrapping Toped

## How To
First you have to Get Product Url by specify some keyword, then Get Product Details using product urls that saved in csv.  

### Get Products Url from Keyword Search
    python main.py --mode url --search_key "Xiaomi note 10" --limit_pages 1

--mode url      : mode to get product urls
--search_key    : keyword , eg. "Xiaomi note 10"
--limit_pages   : limit count of pagination that saved in csv, 
                   put value 0 if you want to save all pages. 

### Get Products Details
    python main.py --mode product 

--mode url      : mode to get product details


Thank you!
