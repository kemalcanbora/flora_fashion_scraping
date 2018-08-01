from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017')
mydb = client["moda_db"]
mycol = mydb["dress"]


def check_data(product_link):
    check = mycol.find({"url": product_link}).count()
    return check

def insert_data(data_dict):
    mycol.insert_many(data_dict)

def find_product_link(img):
    check = mycol.find({"img": str(img)})
    return check[0]["url"]
