import os
import numpy as np
from tensorflow.keras.preprocessing import image as kimage
from model import FeatureExtractor

root_img_path = "../static/img/"
root_fearure_path = "../static/feature/"
dic_categories = ['animal', 'furniture', 'plant', 'scenery']

def folder_to_images(folder):

    list_dir = [folder + '/' + name for name in os.listdir(folder) if name.endswith((".jpg", ".png", ".jpeg"))]
    
    i = 0
    images_np = np.zeros(shape=(len(list_dir), 224, 224, 3))
    images_path = []
    for path in list_dir:
        try:
            img = kimage.load_img(path, target_size=(224, 224))
            images_np[i] = kimage.img_to_array(img, dtype=np.float32)
            # images_np[i] = np.expand_dims(images_np[i], axis=0)
            images_path.append(path)
            i += 1
            
        except Exception:
            print("error: ", path)


    return images_np, images_path


if __name__ == '__main__':

    fe = FeatureExtractor()
    
    # path = 'static\images\plant_Clove'
    # print(path.split("_")[0])

    # fearure_path = root_fearure_path + '*'

    for folder in os.listdir(root_img_path):
        if folder.split("_")[0] in dic_categories:
            path = root_img_path + folder
            images_np, images_path = folder_to_images(path)
            print(root_fearure_path+folder)
            np.savez_compressed(root_fearure_path+folder, array1=np.array(images_path), array2=fe.extract(images_np))