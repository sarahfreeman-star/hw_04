import requests
import json
from bs4 import BeautifulSoup

def ebay_search(query,pages):
    product_list = []
    for i in range(1,pages+1):
        url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw='+query+'&_sacat=1&_pgn='+str(i)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        products = soup.find_all('li', attrs={'class': 's-item'})
        for product in products:  #get all items
            product_dict = {}   #dictionary for each product
            #get product's name
            product_name = product.find_all('h3', attrs={'class':"s-item__title"})
            if(product_name == []):   #if invalid name then skip to the next product
                product_dict['name'] = 'Not Given'
            else: product_dict['name'] = product_name[0].contents[len(product_name[0].contents)-1]

            #get product's price
            product_price = product.find_all('span', attrs={'class':"s-item__price"})
            if(product_name == []):   #if invalid price then skip to the next product
                product_dict['price'] = 'Not Given'
            else: 
                if 'span' in str(product_price[0].contents[0]):
                    product_dict['price'] = product_price[0].contents[0].contents[0]
                else: product_dict['price'] = product_price[0].contents[0]

            #get product's status
            product_status = product.find_all('span', attrs={'class':"SECONDARY_INFO"})
            if(product_status == []):   #if it doesnt have a status then skip to the next product
                product_dict['price'] = 'Not Given'
            else: product_dict['status'] = product_status[0].contents[0]
            product_list.append(product_dict)
    with open('items.json', 'w') as f:
        json.dump(product_list, f)

ebay_search('chocolate',10)
