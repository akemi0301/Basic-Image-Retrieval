import os
import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing import image
from model import FeatureExtractor

root_img_path = "./static/img/"
root_feature_path = "./static/feature/"
dic_categories = ['animal', 'furniture', 'plant', 'scenery']

def folder_to_images(folder, label):

    list_dir = [folder + '/' + name for name in os.listdir(folder) if name.endswith((".jpg", ".png", ".jpeg"))]
    
    i = 0
    images_np = np.zeros(shape=(len(list_dir), 224, 224, 3))
    images_path = []
    labels = []
    for path in list_dir:
        try:
            img = image.load_img(path, target_size=(224, 224))
            images_np[i] = image.img_to_array(img, dtype=np.float32)
            images_np[i] = np.expand_dims(images_np[i], axis=0)
            images_path.append(path)
            labels.append(label)
            i += 1
            
        except Exception:
            print("error: ", path)


    return images_np, images_path, labels


if __name__ == '__main__':

    fe = FeatureExtractor()
    for folder in os.listdir(root_img_path):
        if folder.split("_")[0] in dic_categories:
            label = folder.split("_")[1]
            path = root_img_path + folder
            images_np, images_path, labels = folder_to_images(path, label)
            print(root_feature_path+folder)
            np.savez_compressed(root_feature_path+folder, array1=np.array(images_path), array2=fe.extract(images_np), array3=np.array(labels))