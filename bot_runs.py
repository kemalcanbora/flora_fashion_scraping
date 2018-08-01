from bot_modacruz.modacruz_web_scraping import ModaCruzBot
from bot_zara.zara_web_scraping import ZaraBot
from threading import Thread
from ML import FeatureExtractor

def moda_cruz_bot():
    ModaCruzBot().run(save_path="/static/img/")

def zara_bot():
    ZaraBot().run("/static/img/")

FeatureExtractor().get_all_imgs_feature()
#
# if __name__ == '__main__':
#     cruz_thread = Thread(target = moda_cruz_bot).start()
#     zara_thread = Thread(target = zara_bot).start()
