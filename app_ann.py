import numpy as np
from utils.model import FeatureExtractor
from datetime import datetime
import pandas as pd
from tensorflow.keras.preprocessing import image as kimage
from PIL import Image
from utils.annoy_search import search_index_by_vector

from flask import Flask, url_for, render_template, request, redirect, session
# from flask_ngrok import run_with_ngrok

# Read image features
fe = FeatureExtractor()


root_fearure_path = "./static/features/all_features.npz"

data = np.load(root_fearure_path)

paths_feature = data["paths_feature"]
# print('path images = ',len(paths_feature))

imgs_feature = data["imgs_feature"]
# print('Image features = ', len(imgs_feature))

class_imgs = data["class_imgs"]

def search_and_evalution(img_query):

    topk = 100
    # retrieval_images
    scores, ids, paths  = search_index_by_vector(img_query, topk)
    
    # re-ranking  
    result = pd.DataFrame()
    result['path'] = paths_feature[[idx for idx in ids]]
    result['score'] = scores
    result['rank'] = result['score'].rank(ascending = 1)
    result['class_img_name'] = class_imgs[[idx for idx in ids]]
    result = result.sort_index()

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

    return result, precision
    

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        file = request.files['query_img']

        # Save query image
        img = Image.open(file.stream)  # PIL image
        uploaded_img_path = "static/upload/" + datetime.now().isoformat().replace(":", ".") + "_" + file.filename
        img.save(uploaded_img_path)
        
        # Load query image and FeatureExtractor
        # query = kimage.load_img(uploaded_img_path, target_size=(224, 224))
        # query = kimage.img_to_array(query, dtype=np.float32)
        # query_vector = fe.extract(query[None, :])

        result, presicion = search_and_evalution(uploaded_img_path)
        # Lấy kết quả và gửi đến html
        rs = result[['path','class_compare']]  
        rs = rs.to_records(index=False)
        rs = list(rs)
        precision = "Precision: "+str(presicion)
        return render_template('index_thumb.html',
                            query_path=uploaded_img_path,
                            scores=rs,
                            precision = precision)
    else:
        return render_template('index_thumb.html')
        
if __name__=="__main__":
    
    app.run(host='localhost', port='6868', debug=True)
    # app.run()
