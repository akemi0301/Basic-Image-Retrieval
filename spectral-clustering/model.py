from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
import tensorflow.keras as keras
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
import numpy as np 

# class FeatureExtractor:
    # def __init__(self):
    #     base_model = VGG16(weights='imagenet')
    #     self.model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)

    # def extract(self, img):
    #     """
    #     Extract a deep feature from an input image
    #     Args:
    #         img: from PIL.Image.open(path) or tensorflow.keras.preprocessing.image.load_img(path)

    #     Returns:
    #         feature (np.ndarray): deep feature with the shape=(4096, )
    #     """
    #     x = preprocess_input(img)  # Subtracting avg values for each pixel
    #     feature = self.model.predict(x)[0]  # (1, 4096) -> (4096, )
    #     return feature / np.linalg.norm(feature)  # Normalize

class FeatureExtractor:
    def __init__(self):
        base_model = ResNet50(weights='imagenet', include_top=False)
        x = base_model.output
        x = keras.layers.GlobalAveragePooling2D()(x)
        self.model = keras.Model(inputs=base_model.input, outputs=x)
        
    def extract(self, img):
        
        x = preprocess_input(img)  # Subtracting avg values for each pixel
        feature = self.model.predict(x)
        feature = feature / np.linalg.norm(feature)  # (1, 2048)
        return feature # Normalize
