import numpy as np
import pandas as pd
from PIL import Image
from tensorflow.keras.models import  Model
from tensorflow.keras.preprocessing import image
from flask import Flask, request, render_template
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input


# Ham tao model
def get_extract_model():
    vgg16_model = VGG16(weights="imagenet")
    extract_model = Model(inputs=vgg16_model.inputs, outputs = vgg16_model.get_layer("fc1").output)
    return extract_model

# Ham tien xu ly, chuyen doi hinh anh thanh tensor
def image_preprocess(img):
    img = img.resize((224,224))
    img = img.convert("RGB")
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x
  
# Ham trich xuat dac trung anh
def extract_vector(model, image_path):
    print("Xu ly : ", image_path)
    img = Image.open(image_path)
    img_tensor = image_preprocess(img)
    # Trich dac trung
    vector = model.predict(img_tensor)[0]
    # Chuan hoa vector = chia chia L2 norm (tu google search)
    vector = vector / np.linalg.norm(vector)
    return vector

# Đọc vectors từ file csv
global_df_vectors = pd.read_csv('./static/feature/clusters_img.csv')
# Đọc centroids từ file csv
global_centroids = pd.read_csv('./static/feature/centroids_img.csv')

#Tra cứu ảnh và đánh giá 
def evaluate(image_test, content_img_test, global_df_vectors, global_centroids):
  # Khoi tao model
  model = get_extract_model()

  # Trich dac trung anh search
  search_vector = extract_vector(model,image_test)

  # Đọc vectors từ file csv
  df_vectors = global_df_vectors

  # Đọc centroids từ file csv
  centroids = global_centroids

  # So sánh features của ảnh query với centroid features
  distance = np.linalg.norm(np.array(centroids[centroids.columns[0:4096]])- search_vector, axis=1)

  #Lấy tên cluster min
  min_cluster = list(distance).index(np.min(distance))

  #Lấy ra cluster giống với ảnh query được chọn
  df_vectors = df_vectors[df_vectors["cluster"]== min_cluster]

  #Ranking lại cluster
  distance = np.linalg.norm(np.array(df_vectors[df_vectors.columns[0:4096]])- search_vector, axis=1)
  df_vectors['distance'] = pd.Series(distance, index=df_vectors.index)
  df_vectors['rank'] = df_vectors['distance'].rank(ascending = 1)
  df_vectors = df_vectors.set_index('rank')
  df_vectors = df_vectors.sort_index()

  #Lấy ra cluster giống với ảnh query được chọn
  df_vect = df_vectors[df_vectors["cluster"]== min_cluster]

  #Ranking lại cluster
  distance = np.linalg.norm(np.array(df_vect[df_vect.columns[0:4096]])- search_vector, axis=1)
  df_vect['distance'] = pd.Series(distance, index=df_vect.index)
  df_vect['rank'] = df_vect['distance'].rank(ascending = 1)
  df_vect = df_vect.set_index('rank')
  df_vect = df_vect.sort_index()

  #Lấy ra kết quả tối đa  100 ảnh giống nhất với ảnh query trong cluster
  result = df_vect[0:100] 

  #So sánh với nhãn để đánh giá true/false
  content_compare = []
  for content in result['Content']:
    if str(content) == content_img_test:
      content_compare.append(True)
    else:
      content_compare.append(False)
  result['Content_compare'] = pd.Series(content_compare, index=result.index)
  correct_result=content_compare.count(True)
  precision = correct_result/len(content_compare)
  print('Precision:',precision)
  return result,precision

#build web Flask
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        file = request.files['query_img']
        # Save query image
        img = Image.open(file)  # PIL image
        uploaded_img_path = "static/uploaded/"+ file.filename
        img.save(uploaded_img_path)
        # lấy content là 3 kí tự đầu của tên query image để evaluate kết quả
        content_image = file.filename[0:3] 
        result, ps = evaluate(uploaded_img_path, content_image, global_df_vectors, global_centroids)
        # Lấy kết quả và gửi đến html
        rs = result[['Path','Content_compare']]  
        rs = rs.to_records(index=False)
        rs = list(rs)
        precision = "Precision: "+str(ps)
        return render_template('index.html',
                            query_path=uploaded_img_path,
                            scores=rs,
                            precision = precision)
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
