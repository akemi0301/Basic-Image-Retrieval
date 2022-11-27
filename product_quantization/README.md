## Vector Quantization
Ý tưởng ban đầu sử dụng Vector Quantization. Cụ thể, thay vì tìm kiếm trên 1 tỉ bức ảnh thì ta phân cụm với k-means được 1 triệu cluster chẳng hạn, mỗi cluster ứng với 1 centroid. Khi thực hiện tìm kiếm với query là một bức ảnh, sau khi thực hiện feature engineering thu được 1 vector N chiều, vector đó sẽ được so sánh với các centroid để tìm ra centroid gần nhất. Từ đó, chỉ cần so sánh các ảnh trong cluster đó với query vector. Kĩ thuật này dùng để xấp xỉ 1 vector bằng 1 vector khác, trong trường hợp này là centroid, hay kĩ thuật Vector Quantization. 

Tuy nhiên, việc phân cụm ra 1 triệu cluster và so sánh trong cluster gần nhất vẫn rất tốn thời gian, 1 kĩ thuật đơn giản hơn được đề xuất gọi là Product Quantization. Product Quantization là một trong những phương pháp tỏ ra khá hiệu quả trong việc handing với tập dữ liệu lớn (large-scale data). Mỗi vector sẽ được chia nhỏ (split) và được ánh xạ thành các short code hoặc PQ-code, khi phân cụm ta tiến hành ngay trên tập vector đã được chia nhỏ đó (sub-vectors).

Lấy ví dụ bạn có 1 tập dữ liệu với gồm 50000 ảnh, mỗi ảnh sau khi thực hiện feature extraction qua mạng CNN thu được 1 vector 1024D. Như vậy, ta có 1 ma trận: 50000x1024

![0](https://user-images.githubusercontent.com/85627308/204157125-6b6a0b4b-5972-44bb-ac79-db91e0aca929.png)

Ta tiến hành chia nhỏ (split) từng vector thành 8 tập sub-vectors, mỗi sub-vectors là 128D (128 * 8 = 1024). Khi đó, ta thu được một tập hợp các sub-vectors như hình bên dưới:

![1](https://i.imgur.com/USbxWhz.png)

Ta thực hiện phân cụm với thuật toán k-means với từng tập sub-vectors của 50000 ảnh (ứng với từng cột sub-vectors như hình dưới), kết quả thu được là một tập các cụm của sub-vectors:

![](https://i.imgur.com/fe0VCo0.png)

Khi đó, mỗi cột (8 cột) được gọi là 1 sub-codebook và mỗi cụm (256 cụm mỗi sub-codebook) được gọi là một sub-codeword (mỗi sub-codeword ứng với 1 centroid. Sau khi thu được các cluster và đánh index từ 1->256, ta tính toán theo 2 công thức

![Imgur](https://i.imgur.com/N1HHaeF.png)

![Imgur](https://i.imgur.com/0IbaC6T.png)

thu được short-code tương ứng với vector đầu vào xx (hàng xanh lá cây như hình bên dưới)

![compression](https://i.imgur.com/JbCX9RV.png)

Giả sử với 1 vector ban đầu 1024D 32-bit floats (tương đương 4096 bytes). Sau khi chia nhỏ vector, mỗi sub-vector lại có kích thước 128D 32-bit floats (4096 bytes). Bởi vì, ta có 256 centroid (cluster) nên chỉ cần dùng 8-bits để lưu giữ các centroid id. Với phương pháp Lossy Compression này, ta giảm thiểu được bộ nhớ khi truy vấn đi rất nhiều lần, đồng thời, thời gian tìm kiếm cũng nhanh chóng hơn bằng việc xấp xỉ vector ban đầu bằng PQ-code.
