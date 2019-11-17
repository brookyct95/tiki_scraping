from flask import Flask, render_template, request
from Scrapping import Scraper
app = Flask(__name__)
URL = 'https://tiki.vn/'
#URL_LIST = 
@app.route('/', methods=['GET', 'POST'])
def index():
  tiki_scraper = Scraper()
  table = [tiki_scraper.scrape_page(URL).to_html(classes='data', header="true")]
  if request.method == 'POST':
    url = request.form['tiki_url']
    if request.form['submit-button'] == 'scrape-page':
      data = tiki_scraper.scrape_page(url)
      table = [data.to_html(classes='data', header="true")]
    elif request.form['submit-button'] == 'scrape-category':
      data = tiki_scraper.scrape_page(URL)
      table = [tiki_scraper.scrape_category(url).to_html(classes='data', header="true")]
    elif request.form['submit-button'] == 'scrape-all':
      data = tiki_scraper.scrape_page(URL)
      table = [tiki_scraper.scrape_all().to_html(classes='data', header="true")]
  elif request.method == 'GET':
    data = tiki_scraper.scrape_page(URL)
  return render_template('index.html',data = data, tables=table)

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 