import tensorflow.keras as keras
import os
import numpy as np
from tensorflow.keras.preprocessing import image as kimage
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input

class FeatureExtractor:
    def __init__(self):
        base_model = ResNet50(weights="weight_resnet50.h5", include_top=False)
        x = base_model.output
        x = keras.layers.GlobalAveragePooling2D()(x)
        self.model = keras.Model(inputs=base_model.input, outputs=x)
        
    def extract(self, img):
        
        x = preprocess_input(img)  # Subtracting avg values for each pixel
        feature = self.model.predict(x)  # (1, 2048)
        return feature # Normalize

root_img_path = "static/images/"
root_fearure_path = "static/feature/"
dic_categories = ['scenery', 'furniture', 'animal', 'plant']

def folder_to_images(folder):
    
    list_dir = [folder + '/' + name for name in os.listdir(folder) if name.endswith((".jpg", ".png", ".jpeg"))]
    
    i = 0
    images_np = np.zeros(shape=(len(list_dir), 224, 224, 3))
    images_path = []
    for path in list_dir:
        try:
            img = kimage.load_img(path, target_size=(224, 224), )
            images_np[i] = kimage.img_to_array(img, dtype=np.float32)
            images_path.append(path)
            i += 1
            
        except Exception:
            print("error: ", path)
    #         os.remove(root_img_path + img_path)

    images_path = np.array(images_path)
    return images_np, images_path


if __name__ == '__main__':

    fe = FeatureExtractor()
    
    for folder in os.listdir(root_img_path):
        if folder.split("_")[0] in dic_categories:
            path = root_img_path + folder
            images_np, images_path = folder_to_images(path)
            np.savez_compressed(root_fearure_path+folder, array1=np.array(images_path), array2=fe.extract(images_np))
        
