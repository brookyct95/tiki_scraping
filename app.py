from flask import Flask, render_template, request
from Scrapping import Scraper
import Utilities, Category, Product
import pandas as pd
app = Flask(__name__)
URL = 'https://tiki.vn/'
db_uri = 'postgres://brook:1234@127.0.0.1:5432/tiki_scraping'
#URL_LIST = 
@app.route('/', methods=['GET', 'POST'])
def index():
  table_names = 'products'
  table = pd.read_sql_table(table_names,db_uri)
  if request.method == 'POST':
    query = request.form['query']
    word_list = query.split()
    for i in range(len(word_list)-1):
      if word_list[i] == "FROM" or word_list[i] == "From":
        table_names = word_list[i+1].upper()
        break
    table = pd.read_sql_query(query,db_uri)
  # if request.method == 'POST':
  #   url = request.form['tiki_url']
  #   if request.form['submit-button'] == 'scrape-page':
  #     table = [data.to_html(classes='data', header="true")]
  #   elif request.form['submit-button'] == 'scrape-category':
  #     table = [tiki_scraper.scrape_category(url).to_html(classes='data', header="true")]
  #   elif request.form['submit-button'] == 'scrape-all':
  #     table = [tiki_scraper.scrape_all().to_html(classes='data', header="true")]
  # elif request.method == 'GET':
  #   pass
  return render_template('index.html', tables=[table.to_html(classes='mystyle', header="true")], name = table_names)

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 