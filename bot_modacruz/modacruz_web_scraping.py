import bs4
import requests
from os import remove
import uuid,re
from config import  *
from mongo_querys import  check_data,insert_data
import json
from image_size_down import size_down

brand_name = "Moda Cruz"

class ModaCruzBot:
    def __init__(self):
        print("Moda Cruz Bot Run!")

    def find_img_url_with_modacruz_link(self,URL,save_path):
        img_list = []
        r = requests.get(URL,headers=HEADERS_GET)
        if r.status_code == 200 :
            soup = bs4.BeautifulSoup(r.text,"html.parser")
            for img in soup.find_all("a",{"class":"item fancybox-buttons"}):
                img_url = "http:" + img["href"]
                r = requests.get(img_url, headers=HEADERS_GET)
                image_name = uuid.uuid4().hex + '.jpg'
                open(save_path + image_name, 'wb').write(r.content)
                size_down(save_path + image_name)
                img_list.append(image_name)

            return img_list

    def find_product_name_with_url(self,URL):
        r = requests.get(URL,headers=HEADERS_GET)
        if r.status_code == 200:
            soup = bs4.BeautifulSoup(r.text, 'lxml')
            return soup.find("h1").get_text().lower()

    def run(self,save_path):

        for product_url in moda_cruz_category_url_list:
            for page_number in range(CRUZ_START_PAGE, CRUZ_END_PAGE):
                page_no = "?pg={}".format(page_number)
                r = requests.get(product_url+page_no, headers=HEADERS_GET)
                print(r.url)
                soup = bs4.BeautifulSoup(r.text,"lxml")
                for td in soup.find_all("div",{"class":"card-content"}):
                    modacruz_list = []
                    product_href = td.find('a', href=re.compile(r'[/]([a-z]|[A-Z])\w+')).attrs['href']
                    product_name = self.find_product_name_with_url(product_href)
                    product_img_list = self.find_img_url_with_modacruz_link(product_href,save_path)
                    modacruz_list.append({"img":product_img_list,
                                          "product_name":product_name,
                                          "brand_name":brand_name,
                                          "url":product_href})

                    if len(modacruz_list) != 0:  # liste boş degilse
                        check = check_data(modacruz_list[0]["url"])
                        if check == 0:  # 0 dönerse insert
                            insert_data(json.loads(json.dumps(modacruz_list)))
                        else:
                            if len(modacruz_list) != 0:
                                modacruz_img = modacruz_list[0]["img"]
                                for img in modacruz_img:
                                    remove(save_path + img)
                                    print("Silindi!")


