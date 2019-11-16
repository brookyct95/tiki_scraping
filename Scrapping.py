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

    def scrape_page(self):
        id_list, name_list, category_list, brand_list, img_link_list, price_list, item_link_list,rating_list,no_review_list, tikinow_list =[], [], [],[],[],[],[],[],[],[]
        item_generals = self.soup.findAll('div',class_ = 'product-item')
        for item in item_generals:
            id_list.append(item['data-id'])
            name_list.append(item['data-title'].strip(' '))
            category_list.append(item['data-category'])
            brand_list.append(item['data-brand'])
            price_list.append(item['data-price'])
            img_link_list.append(item.img['src'])
            item_link_list.append(item.a['href'])
            rating_list.append(item.find('span', class_='rating-content').span['style'][-4:].strip(' %:'))
            no_review_list.append(item.find('p', class_='review').text.split()[0].strip('()'))
            tikinow_list.append(1 if item.find('i', class_='tikicon icon-tikinow') else 0)
        data = pd.DataFrame({'id':id_list, 
                            'name':name_list, 
                            'category':category_list, 
                            'brand':brand_list, 
                            'item_link':item_link_list, 
                            'img_link':img_link_list, 
                            'price':price_list,
                            'rating':rating_list,
                            'review':no_review_list,
                            'tikinow':tikinow_list})
        return data
    
    def scrape_category(self):
        pass

    def scrape_all(self):
        pass
