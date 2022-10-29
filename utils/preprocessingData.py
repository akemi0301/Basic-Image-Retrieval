import os
import pandas as pd
from PIL import Image
import numpy as np
import warnings
warnings.filterwarnings("ignore", "(Possibly )?corrupt EXIF data", UserWarning)
Image.MAX_IMAGE_PIXELS = None

def export_csv(root_imgs_path, csv_name):
    dic_categories = {'scenery' : [], 'furniture' : [], 'animal' : [], 'plant' : []}
    
    for path in os.listdir(root_imgs_path):
        c, name = path.split("_")
        if c in dic_categories.keys():
            dic_categories[c].append(name)
    
    # Show information
    total_objects = sum([len(dic_categories[c]) for c in dic_categories])
    # Object có số lượng ảnh lớn nhất 
    max_len = max([len(dic_categories[c]) for c in dic_categories])
    print(f'total_objects = {total_objects}')
    print(f'object có nhiều ảnh nhất = {max_len}')
    
    # generate csv with pandas
    for c in dic_categories:
        dic_categories[c] += [""]*(max_len - len(dic_categories[c]))
    df = pd.DataFrame(dic_categories)
    df.to_csv("categories.csv", index=False)
    
    return dic_categories

def processing_data(images_path):
    dic_categories = {'animal' : [], 'plant' : [], 'furniture' : [], 'scenery' : []}
    count = 0
    
    for folder in os.listdir(images_path):
        if folder.split("_")[0] in dic_categories:
            path = images_path + folder
            list_dir = [path + '/' + name for name in os.listdir(path) if name.endswith((".jpg", ".png", ".jpeg"))]
            for p in list_dir:
                try:
                    #Step1:Open image, sử dụng Image của PIL để mở file ảnh theo path(biến p) 
                    #thu được biến img chứa ảnh(lưu ý: biến thu được chứa ảnh dạng PIL)
                    img = Image.open(p) 
                    
                    #Step2: Verify image, Sau khi mở ảnh ở step1, thu được biến img chứa ảnh, 
                    # .verify(): phát hiện ảnh lỗi
                    img.verify()
                                        
                    #Step3: Open image, Vì sau khi verify() hình ảnh sẽ bị đóng lại, vì vậy cần mở lại hình ảnh như Step1.
                    img = Image.open(p) 
                    
                    #Step4: Check width of image, nếu hình ảnh có width<10 thì xoá ảnh 
                    if img.size[0] < 10:
                        os.remove(p)

                    
                    #Step5: Only 3 channel image (color image), convert ảnh từ PIL sang numpy
                    #nếu hình ảnh có channel khác 3 thì xóa ảnh.
                    img = np.asarray(img)
                    if img.shape[2] != 3:
                        os.remove(p)
                    
                except Exception as e:
                    print(e)
                    count += 1
                    print("error: ", p)
                    os.remove(p) # Các trường hợp ngoại lệ, ảnh lỗi,... sẽ bị xóa

if __name__ == '__main__':

    root_imgs_path = "./images/"
    csv_name = "categories.csv"
    dic_categories = export_csv(root_imgs_path, csv_name)

    root_imgs_path = "./images/"
    processing_data(images_path=root_imgs_path)
