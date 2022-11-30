## Xây dựng trang web tra cứu ảnh sử dụng phân cụm Spectral Clustering
### 1. Tra cứu ảnh dựa vào nội dung (màu sắc, hình dạng, ...)
![cosine](https://user-images.githubusercontent.com/85627308/204691544-bf49c875-dcd7-40b4-bdcd-1519a1480181.png)

Content-based IR là việc tìm kiếm dựa trên nội dung của ảnh (giá trị các pixel trong ảnh). 
Đại khái, chúng là: sự giống nhau về màu sắc, sự giống nhau về kết cấu và sự giống nhau về phạm trù ngữ nghĩa.
Ví dụ của việc này chính là Google Hình ảnh như query là 1 bức ảnh. Bạn có thể upload bức ảnh hoặc link tới 1 bức ảnh trên internet, Google sẽ trả về các bức ảnh có nội dung tương tự. 


### 2. Tra cứu ảnh sử dụng phân cụm spectral clustering
![specl_tq](https://user-images.githubusercontent.com/85627308/204691602-752d253f-45fd-43d8-a33b-78ad049af8f6.png)

Về bản chất, mỗi ảnh đều đã được biểu diễn bởi 1 vector N chiều. Nhiệm vụ bây giờ là tìm kiếm các vector tương đồng trên toàn bộ tập dữ liệu với các metric quen thuộc như: cosine, euclid, ..  Khi so sánh độ tương đồng giữa 2 ảnh, khoảng cách càng nhỏ chứng tỏ sự tương đồng giữa 2 hay nhiều vector càng cao. 

Tuy nhiên nếu chỉ sử dụng độ tương tự để tìm kiếm và so sánh lần lượt từng vector trên toàn bộ tập dữ liệu thì rất tốn thời gian và tài nguyên để tính toán. Để cải thiện nhược điểm này, rất nhiều phương pháp đã được đề xuất và đem lại hiệu quả tốt hơn, trong đó có phương pháp tra cứu ảnh sử dụng phân cụm.

Thuật toán Spectral Clustering sẽ phân các bức ảnh trong tập ảnh thành các cụm với nội dung liên quan đến nhau, với mỗi cụm có một tâm cụm. Khi tra cứu ảnh, thay vì so sánh tính toán độ tương đồng giữa véc tơ đặc trưng của ảnh truy vấn với từng vector đặc trưng của các bức ảnh trong tập ảnh thì giờ đây ta chỉ phải so sánh nó với véc tơ đặc trưng của tâm của mỗi cụm.


### 3. Thuật toán phân cụm
![dpecl](https://user-images.githubusercontent.com/85627308/204686904-1b29900b-280d-4d48-8853-819da95373e6.png)

Để thực hiện phân cụm phổ, chúng ta cần:
1. Tạo một đồ thị biểu diễn các điểm dữ liệu để phân cụm. Đồ thị G = (V, E) với V là tập gồm các đỉnh, mỗi đỉnh ứng với 1 bức ảnh và E là tập gồm các cạnh. Mỗi cạnh gồm có 2 đỉnh và mỗi đỉnh được kết nối với k-láng giềng gần nhất của nó.
2. Tạo ma trận Laplacian
3. Tính toán k vectơ riêng đầu tiên của ma trận Laplacian của nó để xác định một vectơ đặc trưng cho mỗi cụm. Ở đây ta sẽ đi tính véc tơ riêng và giá trị riêng cho ma trận Laplacian, sau đó lấy ra k vector đầu tiên. Có thể nói việc tính ma trận Laplacian và tính k giá trị riêng và vector riêng của ma trận này là trái tim của thuật toán Spectral Clustering. Các giá trị riêng cho biết các thuộc tính toàn cục không rõ ràng của đồ thị từ cấu trúc cạnh.

4. Chạy k-means trên các tính năng này để phân tách các đối tượng thành k cụm. Từ các cụm đỉnh được phân, ta sẽ tính được tâm của mỗi cụm và lưu trữ vào cơ sở dữ liệu phục vụ cho việc so sánh độ tương tự với ảnh truy vấn ở phần tiếp theo

Ở đây sử dụng thư viện có sẵn của [sklearn.cluster.SpectralClustering](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.SpectralClustering.html)

### 4. So sánh độ tương tự đặc trưng ảnh bằng độ đo Cosine
 Sử dụng độ đo Cosing để tính khoảng cách giữa các tâm cụm và điểm ảnh truy vấn. Chọn lấy ra cụm mà tâm cụm khoảng cách ngắn nhất tới điểm ảnh truy vấn.
 
 Sau khi tìm được cụm gần nhất với điểm ảnh truy vấn rồi. Chúng ta lần nữa sử dụng khoảng cách Cosine để tính khoảng cách giữ điểm ảnh truy vấn và các điểm trong cụm gần nhất đó. Sau đó sắp xếp lại các điểm trong cụm theo thứ tự tăng dần của khoảng cách tới điểm ảnh truy vấn. Mục đích để lấy ra tối đa 100 điểm có khoảng cách gần nhất. Và những điểm đó chính là những ảnh giống với ảnh truy vấn nhất, là kết quả của phương pháp tra cứu ảnh nhanh.
 
### 5. Ưu nhược điểm
**Ưu điểm:**
- Nhanh hơn so với truy vấn trực tiếp từ các CSDL vector đặc trưng
- Độ chính xác tương đối

**Nhược điểm**
- Số lượng cụm như thế nào là tốt.
- Kết quả có thể không phải là ảnh thật sự gần nhất 
- Tốn kém chi phí tính toán đối với dữ liệu lớn

### 6. Tạo web với Flask
![demo_cv1](https://user-images.githubusercontent.com/85627308/202763049-f8f19ab9-e036-45c1-9b61-970a9c96c7ee.png)
