# Basic-Image-Retrieval-
Xây dựng một chương trình cho phép truy vấn hình ảnh sử dụng các phép đo độ tương đồng giữa các hình ảnh (Similarity Measure).

- **Input**: Hình ảnh truy vấn q và bộ dữ liệu C.
- **Output**: Danh sách các hình ảnh c (c ∈ C) có sự tương quan đến hình ảnh truy vấn.

<img width="459" alt="image" src="https://user-images.githubusercontent.com/88385496/198692020-95495c2c-725f-4fd6-b850-7d1bc13238f0.png">

## Step 1: Crawl urls chứa ảnh từ web về, lưu thành file txt.
`python utils/crawl_urls_to_txts.py` 

## Step 2: Lấy ảnh từ file txt đã crawl từ step 1.
`python utils/get_images_from_txts.py`

## Step 3: Tiền xử lý các file ảnh ở step 2.
`python utils/preprocessingData.py`

## Step 4: 

<img width="475" alt="image" src="https://user-images.githubusercontent.com/88385496/198692288-83307a4c-32cc-4fcd-8321-e323eab72ac4.png">
