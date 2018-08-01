from bot_modacruz.modacruz_web_scraping import ModaCruzBot
from bot_zara.zara_web_scraping import ZaraBot
from threading import Thread

def moda_cruz_bot():
    ModaCruzBot().run(save_path="/static/img/")

def zara_bot():
    ZaraBot().run("/static/img/")


if __name__ == '__main__':
     cruz_thread = Thread(target = moda_cruz_bot).start()
     zara_thread = Thread(target = zara_bot).start()
