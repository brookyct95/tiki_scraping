import Utilities, Category

class Item():
    def __init__(self, item_id = None,
                 name = None,
                 category = None, brand= None, 
                 img_link = None,price= None, 
                 item_link =None,rating= None,
                 no_of_review = None, tikinow= None,
                 ):
        self.item_id = item_id
        self.name = name
        self.category = category
        self.brand = brand
        self.img_link = img_link
        self.price = price
        self.item_link = item_link
        self.rating = rating
        self.no_of_review = no_of_review
        self.tikinow = tikinow
    
    def save_into_db(self):
        """
        Save item object into db
        """
        conn = Utilities.get_connection()
        cur = conn.cursor()
        #check if self.url is already on categories table 
            
        query = """INSERT INTO products(item_id,
                                            name,
                                            category,
                                            brand,
                                            item_link,
                                            img_link,
                                            price,
                                            rating,
                                            review,
                                            tikinow)
                        VALUES (%(item_id)s,
                                %(name)s,
                                %(category)s,
                                %(brand)s,
                                %(item_link)s,
                                %(img_link)s,
                                %(price)s,
                                %(rating)s,
                                %(review)s,
                                %(tikinow)s);
                    """
        val = {'item_id':self.item_id,
                  'name':self.name,
                  'category':self.category,
                  'brand':self.brand,
                  'item_link':self.item_link,
                  'img_link':self.img_link,
                  'price':self.price,
                  'rating':self.rating,
                  'review':self.no_of_review,
                  'tikinow':self.tikinow}
        try:
            cur.execute(query, val)
            # Get id of the new row
            print(f'ADDED {self.item_id}')
        except Exception as err:
            print(f'ERROR: {err}')
        conn.commit()
        conn.close()
    
    def __repr__(self):
        return f"""[id: {self.item_id}, name: {self.name},\
                category: {self.category}, brand: {self.brand},\ 
                img: {self.img_link}, price: {self.price},\ 
                link: {self.item_link}, rating: {self.rating},\ 
                review: {self.no_of_review}, tikinow: {('Yes' if self.tikinow else 'No') }]"""

def get_item(item):
    """from Soup.tag element (item) 
    get the information 
    and return Item object"""
    id_ = item['data-id']
    name = item['data-title'].strip(' "')
    category = item['data-category']
    brand = item['data-brand']
    price = item['data-price']
    img_link = item.img['src']
    item_link = item.a['href']
    rating = (item.find('span', class_='rating-content').span['style'][-4:].strip(' %:') if item.find('span', class_='rating-content')!= None else -1)
    review = item.find('p', class_='review').text.split()[0].strip('()')
    if not review[0].isdigit():
        review = 0
    tikinow = (1 if item.find('i', class_='tikicon icon-tikinow') else 0)
    res = Item(item_id = int(id_),
               name= name,
               category= category, brand= brand, 
               img_link= img_link,price= int(price), 
               item_link= item_link,rating= int(rating),
               no_of_review= int(review), tikinow= bool(tikinow))
    return res

def scrape_page(url):    
    soup = Utilities.parser(url)
    print(f'Scrape data from {url}')
    item_list = soup.findAll('div',class_ = 'product-item')
    for item_soup in item_list:
        get_item(item_soup).save_into_db()

def scrape_final_node(url):
    soup = Utilities.parser(url)
    if soup.find(class_ = 'current') == None:
        next_url = url
    elif soup.find(class_ = 'current').text == '1':
        next_url = url
    else:
        for i in range(-1,-1*len(url),-1):
            if not url[i].isdigit():
                next_url = url[:i+1] + '1'
                break
    scrape_page(next_url)
    while True:    
        soup = Utilities.parser(next_url)
        next_url = 'https://tiki.vn'+(soup.find(class_ ='next')['href'] if soup.find(class_ ='next') else '')
        if soup.find(class_ ='next') != None:
            scrape_page(next_url)
        else:
            break

def scrape_category(category):
    url = category.url
    if Utilities.is_final_node(url):
        scrape_final_node(url)
    else:
        sub_categories = Category.get_sub_categories(category)
        for cat in sub_categories:
            scrape_category(cat)