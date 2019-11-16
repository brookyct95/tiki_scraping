from bs4 import BeautifulSoup
import requests
import pandas as pd 
class Scraper():
    response = None
    soup = None
    def __init__(self,url):
        self.url = url
        self.response = requests.get(url)
        self.soup = BeautifulSoup(self.response.text)

    def scrape_data(self):
        id_list, name_list, category_list, brand_list, img_link_list, price_list, item_link_list = [], [], [], [], [], [], []
        item_generals = self.soup.findAll('div',class_ = 'product-item')
        for item in item_generals:
            id_list.append(item['data-id'])
            name_list.append(item['data-title'].strip(' '))
            category_list.append(item['data-category'])
            brand_list.append(item['data-brand'])
            price_list.append(item['data-price'])
            img_link_list.append(item.img['src'])
            item_link_list.append(item.a['href'])
        data = pd.DataFrame({'id':id_list, 
                            'name':name_list, 
                            'category':category_list, 
                            'brand':brand_list, 
                            'item_link':item_link_list, 
                            'img_link':img_link_list, 
                            'price':price_list})
        return data