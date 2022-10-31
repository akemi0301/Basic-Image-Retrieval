## Xây dựng trang web tra cứu ảnh sử dụng phân cụm Spectral Clustering
### 1. Tra cứu ảnh dựa vào nội dung (màu sắc, hình dạng, ...)
![content-based image retrieval](https://images.viblo.asia/1584daee-c9f8-421c-9c26-e37d91387685.png)

### 2. Tra cứu ảnh sử dụng phân cụm spectral clustering
![Tra cứu ảnh sử dụng phân cụm Spectral Clustering](https://images.viblo.asia/bc389437-ea9f-45f5-9d9e-61472aa87e77.png)

Ta coi tập ảnh như là một đồ thị, với mỗi đỉnh của đồ thị ứng với một bức ảnh. Thuật toán Spectral Clustering phân cụm đồ thị sẽ phân các bức ảnh trong tập ảnh thành các cụm với nội dung liên quan đên nhau, với mỗi cụm có một tâm cụm. 

Khi tra cứu ảnh, thay vì so sánh tính toán độ tương đồng giữa véc tơ đặc trưng của ảnh truy vấn với từng véc tơ đặc trưng của các bức ảnh trong tập ảnh thì giờ đây ta chỉ phải so sánh nó với véc tơ đặc trưng của tâm của mỗi cụm.

### 3. Trích xuất đặc trưng ảnh bằng VGG16
![vgg16_model](https://www.bangkokmedjournal.com/storage/BKKMEDJ-15-1/15-1-1/15-1-1-F1.jpg)

Sử dụng pretrained VGG16 ImageNet để trích xuất đặc trưng từ ảnh truy vấn và tập ảnh. 
Với tập ảnh, các véc tơ đặc trưng được trích xuất sẽ được lưu lại thành cơ sở dữ liệu đặc trưng. Các véc tơ đặc trưng được trích xuất sẽ lưu vào dưới dạng một DataFrame.

### 4. Phân cụm tập ảnh với Spectral clustering
 Sau quá trình trích xuất, chúng ta sẽ có n véc tơ đặc trưng tương ứng với n ảnh trong tập ảnh. Biểu diễn dưới dạng đồ thị sẽ là n đỉnh của đồ thị G trong không gian 4096 chiều. 
 
 Với đồ thị G này, cho vào model Spectral Clustering sẽ phân được các đỉnh trong G thành các cụm. Bằng việc biểu diễn đồ thị G sang ma trận kề, tính ma trận Laplacian, chọn ra k véc tơ riêng của ma trận Laplacian, thuật toán đã ánh xạ dữ liệu sang một chiều thấp hơn, có tính phổ (bởi các giá trị riêng) để phân cụm dễ dàng hơn với K-means sau đó. Từ các cụm đỉnh được phân, ta sẽ tính được tâm của mỗi cụm, phục vụ cho việc so sánh độ tương tự với ảnh truy vấn ở phần tiếp theo.
 
 ### 5. So sánh độ tương tự đặc trưng ảnh bằng độ đo Euclid
 Sử dụng độ đo Euclid để tính khoảng cách giữa các tâm cụm và điểm ảnh truy vấn. Chọn lấy ra cụm mà tâm cụm khoảng cách ngắn nhất tới điểm ảnh truy vấn.
 
 Sau khi tìm được cụm gần nhất với điểm ảnh truy vấn rồi. Chúng ta lần nữa sử dụng khoảng cách Euclid để tính khoảng cách giữ điểm ảnh truy vấn và các điểm trong cụm gần nhất đó. Sau đó sắp xếp lại các điểm trong cụm theo thứ tự tăng dần của khoảng cách tới điểm ảnh truy vấn. Mục đích để lấy ra tối đa 100 điểm có khoảng cách gần nhất. Và những điểm đó chính là những ảnh giống với ảnh truy vấn nhất, là kết quả của phương pháp tra cứu ảnh nhanh.
 
### Tạo web với Flask

![demo_cv](https://user-images.githubusercontent.com/85627308/198989138-0b810438-cddd-48fb-93b1-8694e75c4b75.png)
