### 1. Vector Quantization
Ý tưởng ban đầu sử dụng Vector Quantization. Cụ thể, thay vì tìm kiếm trên 1 tỉ bức ảnh thì ta phân cụm với k-means được 1 triệu cluster chẳng hạn, mỗi cluster ứng với 1 centroid. Khi thực hiện tìm kiếm với query là một bức ảnh, sau khi thực hiện feature engineering thu được 1 vector N chiều, vector đó sẽ được so sánh với các centroid để tìm ra centroid gần nhất. Từ đó, chỉ cần so sánh các ảnh trong cluster đó với query vector. Kĩ thuật này dùng để xấp xỉ 1 vector bằng 1 vector khác, trong trường hợp này là centroid, hay kĩ thuật Vector Quantization. 

Tuy nhiên, việc phân cụm ra 1 triệu cluster và so sánh trong cluster gần nhất vẫn rất tốn thời gian, 1 kĩ thuật đơn giản hơn được đề xuất gọi là Product Quantization. Product Quantization là một trong những phương pháp tỏ ra khá hiệu quả trong việc handing với tập dữ liệu lớn (large-scale data). Mỗi vector sẽ được chia nhỏ (split) và được ánh xạ thành các short code hoặc PQ-code, khi phân cụm ta tiến hành ngay trên tập vector đã được chia nhỏ đó (sub-vectors).

### 2. Thuật toán Product Quantization

![pq](https://user-images.githubusercontent.com/85627308/204690397-76b29d38-16f6-4f21-b835-d15a5e465eac.png)

**Tham khảo:**

[1] [A Survey of Product Quantization](https://www.jstage.jst.go.jp/article/mta/6/1/6_2/_pdf/)

[2] [Product quantization for similarity search](https://towardsdatascience.com/product-quantization-for-similarity-search-2f1f67c5fddd)


### 3. Đánh giá

**Ưu điểm:**
Tiết kiệm khong gian bộ nhớ: Vì mỗi vectơ trong cơ sở dữ liệu được chuyển đổi thành một short code (PQ code), một biểu diễn cực kỳ hiệu quả về bộ nhớ để tìm kiếm lân cận gần nhất. Như đã minh họa trong ví dụ này, mức sử dụng bộ nhớ giảm tới 64 lần (từ 512 byte xuống 8 byte cho mỗi vectơ) và đó là một lượng đáng kể khi xử lý dữ liệu lớn

**Nhược điểm:**
Việc tìm kiếm chưa tối ưu: Vì tra cứu khoảng cách và tính tổng cần phải được thực hiện cho tất cả các hàng của PQ code.
Độ chính xác mang tính tương đối: Vì chúng ta đang so sánh khoảng cách giữa vectơ với tâm, nên khoảng cách không chính xác là khoảng cách giữa vectơ với vectơ. Chúng chỉ là khoảng cách ước tính, và do đó kết quả có thể ít chính xác hơn và có thể không phải lúc nào cũng là những ảnh thực sự gần nhất.


Chất lượng tìm kiếm có thể được cải thiện bằng cách điều chỉnh số lượng trọng tâm hoặc số lượng phân đoạn. Nhiều trọng tâm hoặc phân đoạn dẫn đến độ chính xác và độ chính xác cao hơn, nhưng chúng cũng sẽ làm chậm hoạt động tìm kiếm cũng như thời gian cần thiết để đào tạo và mã hóa. Ngoài ra, nhiều trọng tâm hơn có thể dẫn đến sự gia tăng số lượng bit cần thiết để biểu diễn mã và do đó tiết kiệm bộ nhớ ít hơn.

