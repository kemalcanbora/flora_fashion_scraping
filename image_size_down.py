from PIL import Image
import os
import glob

def size_down(img):
    byte_size = os.path.getsize(img)
    image = Image.open(img)
    image.thumbnail((224, 224), Image.ANTIALIAS)
    image.save(img, quality=100)
#
# i= 0
# for img_path in sorted(glob.glob('static/img/*.jpg')):
#     i = i+1
#     try:
#         size_down(img_path)
#         print(img_path)
#         print(i)
#     except:
#         continue