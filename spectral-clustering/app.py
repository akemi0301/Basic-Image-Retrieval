import numpy as np
import pandas as pd
from PIL import Image
from datetime import datetime
from tensorflow.keras.preprocessing import image
from flask import Flask, request, render_template
from model import FeatureExtractor
from sklearn.metrics.pairwise import cosine_similarity

fe = FeatureExtractor()

# Đọc vectors từ file csv
global_df_vectors = pd.read_csv('./static/cluster/clusters_30.csv')
# Đọc centroids từ file csv
global_centroids = pd.read_csv('./static/cluster/centroids_30.csv')

#Tra cứu ảnh và đánh giá 
def search_evaluate(search_vector, global_df_vectors, global_centroids):

  # Đọc vectors từ file csv
  df_vectors = global_df_vectors
  # Đọc centroids từ file csv
  centroids = global_centroids
  # Tính khoảng cách giữa các tâm cụm và điểm ảnh truy vấn
  # distance = np.linalg.norm(np.array(centroids[centroids.columns[0:2048]])- search_vector, axis=1)
  distance = np.linalg.norm(1- cosine_similarity(centroids[centroids.columns[0:2048]], search_vector),axis =1)
  print(distance)

  #Lấy tên cluster có tâm cụm min
  min_cluster = list(distance).index(np.min(distance))
  print(min_cluster)

  #Lấy ra các cụm gần nhất với điểm ảnh truy vấn
  df_vectors = df_vectors[df_vectors["cluster"]== min_cluster]
  print(df_vectors.describe(include="all"))

  # Tính khoảng cách giữ điểm ảnh truy vấn và các điểm trong cụm gần nhất đó
  # distance = np.linalg.norm(np.array(df_vectors[df_vectors.columns[0:2048]])- search_vector, axis=1)
  distance = np.linalg.norm(1- cosine_similarity(df_vectors[df_vectors.columns[0:2048]], search_vector),axis =1)
  df_vectors['distance'] = pd.Series(distance, index=df_vectors.index)
  
  # Sắp xếp lại các điểm trong cụm theo thứ tự tăng dần của khoảng cách tới điểm ảnh truy vấn
  df_vectors['rank'] = df_vectors['distance'].rank(ascending = 1)
  df_vectors = df_vectors.set_index('rank')
  df_vectors = df_vectors.sort_index()

  #Lấy ra kết quả tối đa 100 ảnh giống nhất với ảnh query trong cluster
  result = df_vectors[0:100] 

  content_image = result['label'].iloc[0]
  print(content_image)

  #So sánh với nhãn để đánh giá true/false
  content_compare = []
  for content in result['label']:
    if str(content) == content_image:
      content_compare.append(True)
    else:
      content_compare.append(False)
  result['Content_compare'] = pd.Series(content_compare, index=result.index)
  correct_result=content_compare.count(True)
  precision = correct_result/len(content_compare)
  print('Precision:',precision)
  return result, precision


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

        #Tra cứu ảnh và đánh giá
        result, ps = search_evaluate(query_vector, global_df_vectors, global_centroids)
        # Lấy kết quả và gửi đến html
        rs = result[['img_path','Content_compare']]  
        rs = rs.to_records(index=False)
        rs = list(rs)
        precision = "Precision: "+str(ps)

        return render_template('index_thumb.html',
                            query_path=uploaded_img_path,
                            scores=rs,
                            precision = precision)

    return render_template('index_thumb.html')

if __name__=="__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
