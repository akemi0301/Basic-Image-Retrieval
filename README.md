# Basic-Image-Retrieval
Xây dựng một chương trình cho phép truy vấn hình ảnh sử dụng các phép đo độ tương đồng giữa các hình ảnh (Similarity Measure).

- **Input**: Hình ảnh truy vấn q và bộ dữ liệu C.
- **Output**: Danh sách các hình ảnh c (c ∈ C) có sự tương quan đến hình ảnh truy vấn.

<img width="459" alt="image" src="https://user-images.githubusercontent.com/88385496/198692020-95495c2c-725f-4fd6-b850-7d1bc13238f0.png">
<img width="475" alt="image" src="https://user-images.githubusercontent.com/88385496/198692288-83307a4c-32cc-4fcd-8321-e323eab72ac4.png">

## Download dataset
> Data đã được xử lý, tải [tại đây](https://drive.google.com/file/d/1TtQukE5VE4r7DNZcSJaTpRxH1yaFph1A/view?usp=sharing). Chuyển sang step 4 

## Faiss
Facebook AI Similarity Search (Faiss) là một thư viện sử dụng similiarity search cùng với clustering các vector. Faiss được nghiên cứu và phát triển bởi đội ngũ Facebook AI Research; được viết trong C++ và đóng gói trên môi trường Python. Bộ thư viện bao gồm các thuật toán tìm kiếm vector đa chiều trong similarity search

### Similarity search
Bắt đầu với một tập các vector $x_i$ có **d** chiều, Faiss sẽ tự tạo một cấu trúc dữ liệu từ RAM. Sau đó, vector x mới sẽ được tính toán: 
$$i = argmin_i ||x - x_i||$$
Trong Faiss, đây được gọi là tạo ra **index**, một object có khả năng add các vector $x_i$. 

Phần tính toán argmin được gọi là search trong index Faiss cho phép:
- Trả về nhiều kết quả có độ tương tự giống nhau
- Tìm kiếm nhiều vector cùng một lúc (còn gọi là batch processing)
- Lựa chọn giữa độ chính xác (precision) và tốc độ (accuracy). Ví dụ có thể giảm accuracy 10% để tăng gấp 10 tốc độ hoặc giảm 10 lần bộ nhớ
- ...
<img width = "1080" alt="image" src="https://images.viblo.asia/b8a1a28e-2f91-4d8a-84d6-c950a40693dd.jpg">

Similarity Search hiểu 1 cách đơn giản là đi tìm độ giống nhau giữa bức ảnh query và các bức ảnh khác trong dataset, sau đó trả về kết quả dựa trên sự giống nhau từ cao đến thấp. Khác với Image Classification, mỗi bức ảnh sẽ được phân loại vào 1 hoặc một vài class; với Image Retrieval, khi query là 1 bức ảnh thì kết quả trả về có thể là các bức ảnh thuộc class khác. Tham khảo https://www.facebook.com/machinelearningbasicvn/posts/436628436696993/

Các công cụ AI như mạng CNN được huấn luyện với mô hình deep learning, các ảnh sẽ được trích xuất thành các vector đa chiều với các feature đặc trưng, hay còn gọi là các feature vector. Độ tương đồng của 2 bức ảnh sẽ được so sánh bằng khoảng cách (ex: L2 distance) của 2 feature vector trích xuất từ 2 bức ảnh đó. Những ảnh có distance càng nhỏ thì càng giống nhau nhau; những distance nhỏ nhất sẽ được search bởi thuật toán k-selection.


## Yêu cầu
- python==3.8.10
- `pip install -r requirements.txt`

## Test web + chức năng: 
- Run web: [](http://localhost:6868/)
`python app.py`

# Demo website
- Giao diện của web
<img width="1080" alt="image" src="https://user-images.githubusercontent.com/88385496/203021923-e0a32c0e-de9b-4bdf-9cec-901ab2430029.png">

- Upload ảnh
<img width="1080" alt="image" src="https://user-images.githubusercontent.com/88385496/203022076-4ddf651f-f372-4a91-b12d-41b63517b869.png">

- Kết quả 
<img width="1080" alt="image" src="https://user-images.githubusercontent.com/88385496/203039155-908233bd-8611-4a8a-83af-b7158dc9b14a.png">

##Annoy (Approximate Nearest Neighbors Oh Yeah)
- Approximate Nearest Neighbors Oh Yeah (Annoy) là một thư viện C ++ với các ràng buộc Python để tìm kiếm các điểm trong không gian gần với một điểm truy vấn nhất định. Nó cũng tạo ra các cấu trúc dữ liệu dựa trên tệp chỉ đọc lớn được đưa vào bộ nhớ để nhiều quy trình có thể chia sẻ cùng một dữ liệu.
