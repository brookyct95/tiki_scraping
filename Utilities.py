import pandas as pd
import psycopg2
from bs4 import BeautifulSoup
import requests

def parser(url):
    """
    Convert the url into Beautiful Soup
    """
    #Get the HTML
    try:
        res = requests.get(url)
        res = BeautifulSoup(res.text)
    except Exception as exc:
        print(f'{exc}')
    return res

def get_connection():
    """
    Return connection to pgdb
    """
    try:
        conn = psycopg2.connect(user = "brook",
                                password = '1234',
                                host = "127.0.0.1",
                                port = "5432",
                                database = "tiki_scraping")
    except Exception as exc:
        print(exc)
    return conn

def create_category_table():
    conn = get_connection()
    curs = conn.cursor()
    query = """
        CREATE TABLE IF NOT EXISTS categories(
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            url TEXT,
            parent_id INT,
            final_node BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
    """
    try:
        curs.execute(query)
        conn.commit()
    except Exception as err:
        print(f'ERROR: {err}')
    conn.close()

#Function to create table in Tiki database:
def create_products_table():
    connection = get_connection()
    cursor = connection.cursor()
    query = f"""CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                item_id INT,
                name CHAR(400),
                category CHAR(400),
                brand CHAR(50),
                item_link CHAR(400),
                img_link CHAR(200),
                price INT,
                rating INT,
                review INT,
                tikinow BOOLEAN);"""
    try:
        cursor.execute(query)
        connection.commit()
    except (Exception, psycopg2.Error) as error :
        print ("ERROR Error while connecting to PostgreSQL", error)
        
        # In case of error, cancel all changes made to our database during the connection
        connection.rollback()
        return
    finally:
        connection.close()

def is_final_node(url):
    soup = parser(url)
    first_child = soup.find('div', attrs={"class": "list-group-item is-child"})
    if first_child == None:
        final_node = True
    else:
        first_child_url = 'https://tiki.vn' + first_child.a.get('href')
        final_node =(True if first_child_url == url  else False)
    return final_node