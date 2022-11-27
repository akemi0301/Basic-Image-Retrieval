import numpy as np
import pandas as pd
from PIL import Image
from time import time
from datetime import datetime
from tensorflow.keras.preprocessing import image
from flask import Flask, request, render_template
from model import FeatureExtractor
from sklearn.metrics.pairwise import cosine_similarity
from product_quantization.pq import PQ

pq = PQ()
fe = FeatureExtractor()

global_df_vectors = pd.read_csv('./static/cluster/clusters_30.csv')
global_centroids = pd.read_csv('./static/cluster/centroids_30.csv')

feature_path = "./static/feature/feature_pq.npz"
data_pq = np.load(feature_path)
codeword = data_pq['array1']
pqcode = data_pq['array2']

root_feature_path = "./static/feature/all_features.npz"
data = np.load(root_feature_path)
label = data['class_imgs']
df = pd.DataFrame(data["imgs_feature"])
df['label'] = data["class_imgs"]
df['img_path'] = data["paths_feature"]

# Đánh giá
def search_evaluate(df, query, option = 0):
  if (option == 0): 
    result = direct_search(df, query)
  elif (option == 1):
    result = spectral_clustering_search(query, global_df_vectors, global_centroids)
  elif (option==2):
    result = product_quantization_search(df, query, codeword, pqcode)

  #So sánh với nhãn để đánh giá true/false
  content_image = result['label'].iloc[0]
  # print(content_image)
  content_compare = []
  for content in result['label']:
    if str(content) == content_image:
      content_compare.append(True)
    else:
      content_compare.append(False)

  result['Content_compare'] = pd.Series(content_compare, index=result.index)
  correct_result=content_compare.count(True)
  precision = correct_result/len(content_compare)
  # print('Precision:',precision)

  rs = result[['img_path','Content_compare']]  
  rs = rs.to_records(index=False)
  rs = list(rs)
  return rs, precision

#Tra cứu ảnh trực tiếp từ vector đặc trưng
def direct_search(df, query_vector):
    df_vectors = df
    distance = np.linalg.norm(1- cosine_similarity(df_vectors[df_vectors.columns[0:2048]], query_vector),axis =1)
    df_vectors['distance'] = pd.Series(distance, index=df_vectors.index)
    df_vectors['rank'] = df_vectors['distance'].rank(ascending = 1)
    df_vectors = df_vectors.set_index('rank')
    df_vectors = df_vectors.sort_index()
    result = df_vectors[0:100]
    return result

#Tra cứu ảnh sử dụng thuật toán phân cụm
def spectral_clustering_search(search_vector, global_df_vectors, global_centroids):
  df_vectors = global_df_vectors
  centroids = global_centroids
  distance = np.linalg.norm(1- cosine_similarity(centroids[centroids.columns[0:2048]], search_vector),axis =1)
  min_cluster = list(distance).index(np.min(distance))
  df_vectors = df_vectors[df_vectors["cluster"]== min_cluster]
  distance = np.linalg.norm(1- cosine_similarity(df_vectors[df_vectors.columns[0:2048]], search_vector),axis =1)
  df_vectors['distance'] = pd.Series(distance, index=df_vectors.index)
  df_vectors['rank'] = df_vectors['distance'].rank(ascending = 1)
  df_vectors = df_vectors.set_index('rank')
  df_vectors = df_vectors.sort_index()
  result = df_vectors[0:100]
  return result

#Tra cứu ảnh sử dụng thuật toán product quanlization
def product_quantization_search(df, query, codeword, pqcode):
    query_vector = query[0]
    dist = pq.search(codeword, pqcode, query_vector)
    df_vectors = df
    df_vectors['distance'] = pd.Series(dist, index=df_vectors.index)
    df_vectors['rank'] = df_vectors['distance'].rank(ascending = 1)
    df_vectors = df_vectors.set_index('rank')
    df_vectors = df_vectors.sort_index()
    result = df_vectors[0:100]
    return result

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
        query = fe.extract(query[None, :])

        #Tra cứu ảnh và đánh giá
        start_time = datetime.now()
        result, ps = search_evaluate(df, query, 0)
        end_time = datetime.now()
        time = end_time - start_time
        print("Time: ", time, "seconds")

        # Lấy kết quả và gửi đến html
        precision = "Precision: "+str(ps)
        time = "Time: "+str(time)+ "seconds"

        return render_template('index_thumb.html',
                            query_path=uploaded_img_path,
                            scores = result,
                            precision = precision,
                            time = time)

    return render_template('index_thumb.html')

if __name__=="__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)