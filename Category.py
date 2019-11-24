import pandas as pd
import psycopg2
from bs4 import BeautifulSoup
import requests
import Utilities

class Category:
    def __init__(self, cat_id, name, url, parent_id, final_node = False):
        self.cat_id = cat_id
        self.name = name
        self.url = url
        self.parent_id = parent_id
        self.final_node = final_node
        
    def save_into_db(self):
        conn = Utilities.get_connection()
        cur = conn.cursor()
        #check if self.url is already on categories table 
        query = 'SELECT url FROM categories WHERE url LIKE %s;'
        val = (self.url,)
        try:
            cur.execute(query, val)
            result = cur.fetchall()
            if len(result) > 0:
                return ''
        except Exception as err:
            print(f'ERROR: {err}')
            
        query = f"""
            INSERT INTO categories (name, url, parent_id,final_node) 
            VALUES (%s, %s, %s, %s) RETURNING id;
        """
        val = (self.name, self.url, self.parent_id, self.final_node)
        try:
            cur.execute(query, val)
            # Get id of the new row
            self.cat_id = cur.fetchone()[0]
        except Exception as err:
            print(f'ERROR: {err}')
        print(f'ADDED {self}')
        conn.commit()
        conn.close()
        
    def __repr__(self):
        return f'ID: {self.cat_id}, Name: {self.name}, URL: {self.url}, Parent ID: {self.parent_id}, Final node: {self.final_node}'

def get_main_categories(save_db=False):
    # Run Parser on Tiki
    s = Utilities.parser('https://tiki.vn')
    
    # Initialize an empty list of category 
    category_list = []

    # Scrape through the navigator bar on Tiki homepage
    for i in s.findAll('a',{'class':'MenuItem__MenuLink-tii3xq-1 efuIbv'}):
        # new category has no id
        cat_id = None
        
        # Get the category name
        name = i.find('span',{'class':'text'}).text 
        
        # Get the url value
        url = i['href'] + "&page=1"
        
        # main categories has no parent
        parent_id = None
        
        # Add category and url values to list
        cat = Category(None, name, url, parent_id)
        if save_db:
            cat.save_into_db()
        category_list.append(cat)
        
    return category_list

def get_sub_categories(category):
    name = category.name
    url = category.url
    sub_categories = []
    try:
        div_containers = Utilities.parser(url).find_all('div', attrs={"class": "list-group-item is-child"})
        for div in div_containers:
            sub_id = None
            sub_name = div.a.text
            sub_url = 'https://tiki.vn' + div.a.get('href')
            sub_parent_id = category.cat_id
            cat = Category(sub_id, sub_name, sub_url, sub_parent_id)
            sub_categories.append(cat)
    except Exception as err:
        print(f'ERROR: {err}')
    
    return sub_categories

def get_all_sub_categories(category):
    print(f'checking: {category.url}')
    soup = Utilities.parser(category.url)
    first_child = soup.find('div', attrs={"class": "list-group-item is-child"})
    if first_child == None:
        final_node = True
    else:
        first_child_url = 'https://tiki.vn' + first_child.a.get('href')
        final_node =(True if first_child_url == category.url  else False)
    if final_node:
            category.final_node = True
            category.save_into_db()
    else:
        category.save_into_db()
        sub_categories = get_sub_categories(category)
        for cat in sub_categories:
            get_all_sub_categories(cat)