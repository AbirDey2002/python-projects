import requests
from bs4 import BeautifulSoup

def amazon_scrape(stri):
  url = 'https://www.amazon.in/s?k=' + '+'.join(stri.split())
  
  headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
  }
  

  page = requests.get(url,headers=headers)

  soup1 = BeautifulSoup(page.text, 'html.parser')

  p = soup1.find_all("div",{"data-component-type":"s-search-result"})

  d = []

  for i in range (0,len(p)):
    price = p[i].find('span',class_="a-offscreen").text
    name = p[i].find('span',class_="a-size-medium a-color-base a-text-normal").text
    image = p[i].find("img", attrs={"data-image-source-density":"1"})['src']
    
    d.append(
      {
        'price': price,
        'name': name,
        'image': image
      }
    )
    
  return d