from flask import Flask, jsonify
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


app = Flask(__name__)

def extrair_dados(soup):
    notebooks = []
    for notebook in soup.find_all('div', class_='col-sm-4 col-lg-4 col-md-4'):
        name = notebook.text
        price = notebook.select_one('.price').get_text()
        if 'Lenovo' in name:
            notebooks.append({'name': name, 'price': price})
    return notebooks

@app.route('/', methods=['GET'])
def notebooks():
    service = Service(executable_path='C:/Users/yghor/Desktop/Yghor/robo_webScraper/chromedriver/chromedriver.exe')
    service.start()
    driver = webdriver.Chrome(service=service)
    driver.get('https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops')
    buscar_pagina = driver.page_source
    soup = BeautifulSoup(buscar_pagina, 'html.parser')

    notebooks = extrair_dados(soup)
    driver.quit()
    notebooks.sort(key=lambda x: float(x['price'].replace(',','').replace('$','')))
    return jsonify(notebooks)

if __name__ == '__main__':
    app.run(debug=True)















