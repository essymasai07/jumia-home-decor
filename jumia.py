import pandas as pd
from bs4 import BeautifulSoup
import requests

name = []
old_price = []
current_price = []
discount = []

page = 1
isthereanextpage = True

while isthereanextpage:
    url = f'https://www.jumia.co.ke/artificial-plants/?page={page}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    products = soup.find_all('article', class_="prd _fb col c-prd")
    
    for item in products:
        names = item.find('h3', class_='name').text.strip()
        old_prices = item.find('div', class_='old').text.strip() if item.find("div", class_="old") else ""
        current_prices = item.find('div', class_='prc').text.strip()
        discounts = item.find('div', class_='bdg _dsct _sm')
        if discounts is not None:
            discounts = discounts.string.strip()
        else:
            discounts = None
            
        name.append(names)
        old_price.append(old_prices)
        current_price.append(current_prices)
        discount.append(discounts)
    
    next_page = soup.find('a', {'aria-label': 'Next Page'})
    isthereanextpage = next_page is not None
    page += 1

df = pd.DataFrame({'Product Name': name, 'Old Price': old_price, 'Current Price': current_price, 'Discount': discount})
df.to_csv('Home Decor.csv', index=False, encoding='utf-8')
print('data has been saved')