import numpy as np
import pandas as pd
from PIL import Image
from datetime import datetime
from tensorflow.keras.preprocessing import image
from flask import Flask, request, render_template
from model import FeatureExtractor
from scipy.spatial import distance

# Đọc vectors từ file csv
global_df_vectors = pd.read_csv('./static/feature/clusters.csv')
# Đọc centroids từ file css
global_centroids = pd.read_csv('./static/feature/centroids.csv')

folder_query = "query_pic/"

root_feature_path = "./static/feature/all_features.npz"

data = np.load(root_feature_path)
paths_feature = data["array1"]
imgs_feature = data["array2"]

fe = FeatureExtractor()

def cosine_similarity(query, X):
    norm_2_query = np.sqrt(np.sum(query*query))
    norm_2_X = np.sqrt(np.sum(X*X, axis=-1))
    return np.sum(query*X, axis=-1)/(norm_2_query*norm_2_X)

def retrieval_images(query_vector, imgs_feature):
    # caculate similarity between query and features in database
    rates = cosine_similarity(query_vector, imgs_feature)
    id_s = np.argsort(-rates)[:100] # Top 30 results
    return [(round(rates[id], 2), paths_feature[id]) for id in id_s]

def euclid_similarity(df, X):
    return np.linalg.norm(np.array(df[df.columns[0:2048]])- X, axis=1)

def ranking_cluster(df_vect, search_vector):
  #Ranking lại cluster
  distance = euclid_similarity(df_vect, search_vector)
  df_vect['distance'] = pd.Series(distance, index=df_vect.index)
  df_vect['rank'] = df_vect['distance'].rank(ascending = 1)
  df_vect = df_vect.set_index('rank')
  df_vect = df_vect.sort_index()
  return df_vect

#Tra cứu ảnh
def search_images(search_vector, global_df_vectors, global_centroids):
  # Đọc vectors, centroids từ file csv
  df_vectors = global_df_vectors
  centroids = global_centroids

  # So sánh features của ảnh query với centroid features và lấy tên cluster min
  distance = euclid_similarity(centroids, search_vector)
  min_cluster = list(distance).index(np.min(distance))

  #Lấy ra cluster giống với ảnh query được chọn, ranking lại cluster
  df_vectors = df_vectors[df_vectors["cluster"]== min_cluster]
  df_vectors = ranking_cluster(df_vectors, search_vector)

  #Lấy ra cluster giống với ảnh query được chọn, ranking lại cluster
  df_vect = df_vectors[df_vectors["cluster"]== min_cluster]
  df_vect = ranking_cluster(df_vect, search_vector)

  #Lấy ra kết quả tối đa  100 ảnh giống nhất với ảnh query trong cluster
  return df_vect[0:100] 

# Đánh giá 
def evaluate(result, content_img_test):
  #So sánh với nhãn để đánh giá true/false
  content_compare = []
  for content in result['label']:
    if str(content) == content_img_test:
      content_compare.append(True)
    else:
      content_compare.append(False)
  result['Content_compare'] = pd.Series(content_compare, index=result.index)
  correct_result=content_compare.count(True)
  precision = correct_result/len(content_compare)
  print('Precision:',precision)
  return result,precision

# build web Flask
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])

def index():

    if request.method == 'POST':
        file = request.files['query_img']

        # Save query image
        img = Image.open(file.stream)  # PIL image
        # uploaded_img_path = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + file.filename
        uploaded_img_path = "./static/uploaded/" + file.filename
        img.save(uploaded_img_path)
        
        # Load query image and FeatureExtractor
        query = image.load_img(uploaded_img_path, target_size=(224, 224))
        query = image.img_to_array(query, dtype=np.float32)
        query_vector = fe.extract(query[None, :])

        # retrieval_images
        # scores = retrieval_images(query_vector, imgs_feature)

        # Tra cứu ảnh
        result = search_images(query_vector, global_df_vectors, global_centroids)
        
        # lấy content là 3 kí tự đầu của tên query image để evaluate kết quả
        content_image = result['label'].iloc[0]
        print(content_image)
        result, ps = evaluate(result, content_image)

        # Lấy kết quả và gửi đến html
        rs = result[['img_path','Content_compare']]  
        rs = rs.to_records(index=False)
        rs = list(rs)
        precision = "Precision: "+str(ps)

        return render_template('index.html',
                            query_path=uploaded_img_path,
                            scores=rs,
                            precision = precision)

        # return render_template('index_thumb.html',
        #                        query_path=uploaded_img_path,
        #                        scores1=rs[:10],
        #                        scores2=rs[10:20],
        #                        scores3=rs[20:])

    return render_template('index.html')

if __name__=="__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
