import tensorflow as tf
from model import FeatureExtractor
import os
import numpy as np
from tensorflow.keras.preprocessing import image as kimage

root_img_path = "../static/img/"
root_feature_path = "../static/feature/"
dic_categories = ['scenery', 'furniture', 'animal', 'plant']

if __name__ == '__main__':
    
    imgs_feature = []
    paths_feature = []

    # for path in os.listdir(root_fearure_path):
    #     if path.endswith(".npz"):
    #         print(path)

    for path in [root_feature_path + path for path in os.listdir(root_feature_path) if path.endswith(".npz")]:
        data = np.load(path)
        paths_feature.extend(data["array1"])
        imgs_feature.extend(data["array2"])

    np.savez_compressed(root_feature_path+"all_feartures", array1=np.array(paths_feature), array2=np.array(imgs_feature))
    print("Done!")

