from flask import Flask, render_template
from Scrapping import Scraper
app = Flask(__name__)
URL = 'https://tiki.vn/dien-thoai-may-tinh-bang/c1789?src=c.1789.hamburger_menu_fly_out_banner'

@app.route('/')
def index():
  tiki_scraper = Scraper(URL)
  data = tiki_scraper.scrape_page()
  return render_template('index.html',data = data)

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 