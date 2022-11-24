import os
import numpy as np
from pathlib import Path

root_img_path = "./static/img/"
root_feature_path = "./static/feature/"
dic_categories = ['scenery', 'furniture', 'animal', 'plant']

if __name__ == '__main__':
    
    imgs_feature = []
    paths_feature = []
    class_imgs = []

    for path in [root_feature_path + path for path in os.listdir(root_feature_path) if path.endswith(".npz")]:
        data = np.load(path)
        paths_feature.extend(data["array1"])
        imgs_feature.extend(data["array2"])

    for path in paths_feature:
        class_img = path.split("/")[-2]
        class_imgs.append(class_img)

    np.savez_compressed(root_feature_path+"all_features", paths_feature=np.array(paths_feature), imgs_feature=np.array(imgs_feature), class_imgs=np.array(class_imgs))
    print("Done!")
