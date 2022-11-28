import numpy as np 
from annoy import AnnoyIndex
from tqdm import tqdm
import torch
import pandas as pd
from utils.model import FeatureExtractor
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image as kimage

device = "cuda" if torch.cuda.is_available() else "cpu"

data = np.load("./static/features/all_features.npz")
imgs_feature = data["imgs_feature"]
paths_feature = data["paths_feature"]
ann_file = './static/annoy_L2.ann'
class_imgs = data["class_imgs"]

id2img_fps = dict(enumerate(imgs_feature))

# creat all image file in faiss bin

def create_index(features, n_trees=1000, dims=2048):
    # build the index by dimension and add vectors to the index
    index = AnnoyIndex(dims, metric='euclidean')
    for i, row in enumerate(features):
        vec = row
        index.add_item(i, vec)
    index.build(n_trees)
    # write index file to disk
    index.save('./static/annoy_L2.ann')
    
    print('done!!')

def get_feature_vector(path_image):

    fe = FeatureExtractor()

    query = kimage.load_img(path_image, target_size=(224, 224))
    query = kimage.img_to_array(query, dtype=np.float32)
    query_vector = fe.extract(query[None, :])
    query_vector  = query_vector.reshape(query_vector.shape[1], -1)
    return query_vector

def search_index_by_vector(path_image_query, top_n):
    a = AnnoyIndex(2048, metric="euclidean")
    a.load(ann_file)
    query_feature = get_feature_vector(path_image_query)
    distances = a.get_nns_by_vector(query_feature, top_n, include_distances=True)
    ids  = distances[0]
    distances = distances[1]
    image_paths = [paths_feature[i] for i in ids]
    return distances, ids, image_paths


if __name__ == "__main__":
    
    # #create file bin
    # create_index_vector(imgs_feature)

    # TEST QUERY
    img_query = './static/images/animal_Alligator/0.89070600258874.jpg'
    # create_index(imgs_feature)
    top_n = 10
    d, i, p= search_index_by_vector(img_query, top_n)
    #t = d[[s for s in range(len(d))]]
    #print(t)
    print(d[0])
    #print(i)
    #print(p)
