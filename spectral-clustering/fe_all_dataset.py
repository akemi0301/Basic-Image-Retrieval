
import os
import numpy as np
from pathlib import Path

root_img_path = "./static/img/"
root_feature_path = "./static/feature/"
dic_categories = ['scenery', 'furniture', 'animal', 'plant']

if __name__ == '__main__':
    
    imgs_feature = []
    paths_feature = []
    imgs_label = []

    # for path in os.listdir(root_fearure_path):
    #     if path.endswith(".npz"):
    #         print(path)

    for path in [root_feature_path + path for path in os.listdir(root_feature_path) if path.endswith(".npz")]:
        data = np.load(path)
        paths_feature.extend(data["array1"])
        imgs_feature.extend(data["array2"])
        imgs_label.extend(data["array3"])
    np.savez_compressed(root_feature_path+"all_features", array1=np.array(paths_feature), array2=np.array(imgs_feature), array3=np.array(imgs_label))
    print("Done!")
