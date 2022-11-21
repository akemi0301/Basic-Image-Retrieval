# pip install faiss
import numpy as np 
import faiss
import torch
import pandas as pd
from utils.model import FeatureExtractor
from tensorflow.keras.preprocessing import image as kimage

device = "cuda" if torch.cuda.is_available() else "cpu"

data = np.load("./static/feature/all_features.npz")
imgs_feature = data["imgs_feature"]
paths_feature = data["paths_feature"]
bin_file = './static/faiss_L2.bin'
class_imgs = data["class_imgs"]

id2img_fps = dict(enumerate(imgs_feature))

# creat all image file in faiss bin
def create_index_vector(img_features):
    # build the index by dimension and add vectors to the index
    index = faiss.IndexFlatL2(2048)
    fea = img_features.reshape(img_features.shape[0], -1).astype('float32')
    index.add(fea)
    # write index file to disk
    faiss.write_index(index, './static/faiss_L2.bin')
    print('done!!')

def get_feature_vector(path_image):

    fe = FeatureExtractor()

    query = kimage.load_img(path_image, target_size=(224, 224))
    query = kimage.img_to_array(query, dtype=np.float32)
    query_vector = fe.extract(query[None, :])
    return query_vector


def get_image_feature_vector(img_id):
    img_ids = data["class_imgs"]
    img_ids = list(img_ids['img_ids'])

    img_idx = img_ids.index(img_id)
    img_features = np.load("./static/all_features.npz")

    img_feature = img_features[img_idx].astype(np.float32)

    img_feature = np.expand_dims(img_feature, axis=0)
    return img_feature

def search_vector(path_image, topk):
    index = faiss.read_index(bin_file)
    fea_vector_search = get_feature_vector(path_image)

    # search image by the feature vector
    scores, idx_image = index.search(fea_vector_search, topk) 
    idx_image = idx_image.flatten()

    image_paths = [paths_feature[i] for i in idx_image]
    return scores, idx_image, image_paths

if __name__ == "__main__":
    
    # #create file bin
    # create_index_vector(imgs_feature)

    # TEST QUERY
    img_query = './static/images/animal_Alligator/0.89070600258874.jpg'
    topk = 20

    scores, ids, paths  = search_vector(img_query, topk)
    # print(paths)

    # re-ranking 
    result = pd.DataFrame()
    result['path'] = paths_feature[[idx for idx in ids]]
    result['score'] = scores[[s for s in range(len(scores))]][0]
    result['rank'] = result['score'].rank(ascending = 1)
    result['class_img_name'] = class_imgs[[idx for idx in ids]]
    result = result.sort_index()

    # print(result)

    class_name_top1 = result['class_img_name'][0]

    content_compare = []
    for cls in result['class_img_name']:
        if str(cls) == class_name_top1:
            content_compare.append(True)
        else:
            content_compare.append(False)
    
    result['class_compare'] = content_compare

    correct_result=content_compare.count(True)

    precision = correct_result/len(content_compare)

    print('Precision:',precision)

    # return result, precision
    print(result)







