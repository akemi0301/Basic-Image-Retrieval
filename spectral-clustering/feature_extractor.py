import os
import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing import image
from model import FeatureExtractor

root_img_path = "./static/img/"
root_feature_path = "./static/feature/"
dic_categories = ['animal', 'furniture', 'plant', 'scenery']

def folder_to_images(folder):

    list_dir = [folder + '/' + name for name in os.listdir(folder) if name.endswith((".jpg", ".png", ".jpeg"))]
    i = 0
    images_np = np.zeros(shape=(len(list_dir), 224, 224, 3))
    folder_name = []
    images_path = []
    for path in list_dir:
        try:
            img = image.load_img(path, target_size=(224, 224))
            images_np[i] = image.img_to_array(img, dtype=np.float32)
            images_path.append(path)
            folder_name.append(path.split('/')[-2])
            i += 1
        except Exception:
            print("error: ", path)
    return images_np, images_path, folder_name

if __name__ == '__main__':

    fe = FeatureExtractor()

    for folder in os.listdir(root_img_path):
        if folder.split("_")[0] in dic_categories:
            path = root_img_path + folder
            images_np, images_path, folder_name = folder_to_images(path)
            np.savez_compressed(root_feature_path+folder, array1=np.array(images_path), array2=fe.extract(images_np), array3=np.array(folder_name))

    # path = './static/images/animal_Alligato/0.89070600258874.jpg'
    # p  = path.split('/')[-2]
    # print(p)