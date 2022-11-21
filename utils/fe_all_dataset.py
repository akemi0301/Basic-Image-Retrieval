import tensorflow as tf
from feature_extractor import FeatureExtractor
import os
import numpy as np
from tensorflow.keras.preprocessing import image as kimage

root_img_path = "./static/images/"
root_fearure_path = "./static/feature/file_npz/"
dic_categories = ['scenery', 'furniture', 'animal', 'plant']

def folder_to_images(folder):
    
    list_dir = [folder + '/' + name for name in os.listdir(folder) if name.endswith((".jpg", ".png", ".jpeg"))]
    
    i = 0
    images_np = np.zeros(shape=(len(list_dir), 224, 224, 3))
    images_path = []
    for path in list_dir:
        try:
            img = kimage.load_img(path, target_size=(224, 224))
            images_np[i] = kimage.img_to_array(img, dtype=np.float32)
            images_path.append(path)
            i += 1
            
        except Exception:
            print("error: ", path)
    #         os.remove(root_img_path + img_path)

    images_path = np.array(images_path)
    return images_np, images_path

if __name__ == '__main__':
    
    imgs_feature = []
    paths_feature = []
    class_imgs = []

    # for path in os.listdir(root_fearure_path):
    #     if path.endswith(".npz"):
    #         print(path)

    for path in [root_fearure_path + path for path in os.listdir(root_fearure_path) if path.endswith(".npz")]:
        data = np.load(path)
        paths_feature.extend(data["array1"])
        imgs_feature.extend(data["array2"])

    for path in paths_feature:
        class_img = path.split("/")[-2]
        class_imgs.append(class_img)

    # print(len(class_imgs))
    # print(len(paths_feature))
    # print(len(imgs_feature))
    

    np.savez_compressed("./static/feature/"+"all_features", paths_feature=np.array(paths_feature), imgs_feature=np.array(imgs_feature), class_imgs=np.array(class_imgs))
    print("Done!")
