# Basic-Image-Retrieval
Xây dựng một chương trình cho phép truy vấn hình ảnh sử dụng các phép đo độ tương đồng giữa các hình ảnh (Similarity Measure).

- **Input**: Hình ảnh truy vấn q và bộ dữ liệu C.
- **Output**: Danh sách các hình ảnh c (c ∈ C) có sự tương quan đến hình ảnh truy vấn.

<img width="459" alt="image" src="https://user-images.githubusercontent.com/88385496/198692020-95495c2c-725f-4fd6-b850-7d1bc13238f0.png">
<img width="475" alt="image" src="https://user-images.githubusercontent.com/88385496/198692288-83307a4c-32cc-4fcd-8321-e323eab72ac4.png">

## Download dataset
> Data đã được xử lý, tải [tại đây](https://drive.google.com/file/d/1bPADa_yqvDENnNiRLq__GFn4DrUTt_NY/view?usp=sharing). Chuyển sang step 4 

## Yêu cầu
- python==3.8.10
- `pip install -r requirements.txt`

## Test web + chức năng: 
- Run web: [](http://localhost:6868/)
`python app.py`

# Demo website
- Giao diện của web
<img width="1080" alt="image" src="https://user-images.githubusercontent.com/88385496/198829340-565d3b87-8ce5-4536-8f9c-f9b80c11b434.png">

- Upload ảnh
<img width="1080" alt="image" src="https://user-images.githubusercontent.com/88385496/198829382-bb520312-9433-4545-9dee-93a922bc5fdb.png">

- Kết quả 
<img width="1063" alt="image" src="https://user-images.githubusercontent.com/88385496/198829405-6812e96f-a5b3-48f2-90f8-1d895dae033d.png">

