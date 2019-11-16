from bs4 import BeautifulSoup
import requests
import pandas as pd 
class Scraper():
    def scrape_page(self,url):
        response = requests.get(url)
        try:
            response.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s' % (exc))
        soup = BeautifulSoup(response.text)
        id_list, name_list, category_list, brand_list, img_link_list, price_list, item_link_list,rating_list,no_review_list, tikinow_list =[], [], [],[],[],[],[],[],[],[]
        item_generals = soup.findAll('div',class_ = 'product-item')
        for item in item_generals:
            id_list.append(item['data-id'])
            name_list.append(item['data-title'].strip(' '))
            category_list.append(item['data-category'])
            brand_list.append(item['data-brand'])
            price_list.append(item['data-price'])
            img_link_list.append(item.img['src'])
            item_link_list.append(item.a['href'])
            rating_list.append(item.find('span', class_='rating-content').span['style'][-4:].strip(' %:') if item.find('span', class_='rating-content')!= None else -1)
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
    
    def scrape_category(self,url):
        next_url = url
        data = self.scrape_page(next_url)
        while True:    
            response = requests.get(next_url)
            try:
                response.raise_for_status()
            except Exception as exc:
                print('There was a problem: %s' % (exc))
            soup = BeautifulSoup(response.text)
            next_url = 'https://tiki.vn'+(soup.find(class_ ='next')['href'] if soup.find(class_ ='next') else '')
            if soup.find(class_ ='next') != None:
                print('scrape data from: '+next_url)
                try:
                    temp_data = self.scrape_page(next_url)
                    data = pd.concat([data,temp_data],ignore_index = True)
                    print(data.shape)
                except Exception as exc:
                    print('There was a problem: %s' % (exc))
            else:
                break
        return data
    
    def scrape_all(self):
        data = self.scrape_category('https://tiki.vn')
        link_list = []
        response = requests.get('https://tiki.vn')
        try:
            response.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s' % (exc))
        soup = BeautifulSoup(response.text)
        links = soup.find_all(class_='MenuItem__MenuLink-tii3xq-1 efuIbv')
        for link in links:
            link_list.append(link['href'])
        for link in link_list:
            print('scrape data from ' + link)
            try:
                tempdata = self.scrape_category(link)
                data = pd.concat([data,tempdata], ignore_index = True)
            except Exception as exc:
                print('There was a problem: %s' % (exc))
        return data