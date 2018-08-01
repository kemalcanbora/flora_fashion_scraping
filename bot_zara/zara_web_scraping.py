import bs4
import requests
from os import remove
import uuid
from config import *
from mongo_querys import check_data,insert_data
import json
from image_size_down import size_down

brand_name = "Zara"

class ZaraBot:
    def __init__(self):
        print("Zara Bot Run!")

    def run(self,save_path):
        handler = open("zara_sitemap-tr-en.xml").read()
        soup = bs4.BeautifulSoup(handler, 'lxml')
        for zara_url in soup.find_all('loc'):
            img_div_list = ["main-images"]
            img_list = []
            zara_list = []
            product_name = None

            for images_paths in img_div_list:
                r = requests.get(zara_url.get_text(), headers=HEADERS_GET)
                item_url = r.url
                if r.status_code == 200:
                    soup = bs4.BeautifulSoup(r.text, 'lxml')
                    for name in soup.find_all('h1', {'class': "product-name"}):
                        product_name = name.text.lower()
                    for link in soup.find_all('div', {'id': images_paths}):
                        for img in link.find_all('a', href=True):
                            img_url = "http:"+ img["href"]
                            r = requests.get(img_url, headers=HEADERS_GET)
                            image_name = uuid.uuid4().hex+'.jpg'
                            open(save_path+image_name, 'wb').write(r.content)
                            size_down(save_path+image_name)
                            img_list.append(image_name)

                        zara_list.append({"img":img_list,
                                          "product_name":product_name,
                                          "brand_name":brand_name,
                                          "url":item_url
                                          })

                    if len(zara_list) != 0: # liste boş degilse
                        check = check_data(zara_list[0]["url"])
                        if not check == 1: # True dönerse insert
                            insert_data(json.loads(json.dumps(zara_list)))
                        else:
                            if len(zara_list) != 0:
                                zara_img = zara_list[0]["img"]
                                for img in zara_img:
                                    remove(save_path + img)
                                    print("Silindi!")


