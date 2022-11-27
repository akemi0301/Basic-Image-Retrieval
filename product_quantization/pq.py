import numpy as np
import pandas as pd
from scipy.cluster.vq import vq, kmeans2
from scipy.spatial.distance import cdist

root_feature_path = "./static/feature/"
feature_path = "./static/feature/all_features.npz"
data = np.load(feature_path)
feature = data["imgs_feature"]
label = data['class_imgs']

class PQ:
    def train(self, vec, n_subvect, n_cluster=256):
        '''
        :param M: số lượng sub-vectors của từng vector
        :param Ks: số cluster áp dụng trên từng tập sub-vectors
        '''
        d_subvect = int(vec.shape[1] / n_subvect)  # số chiều 1 sub-vector
        print(d_subvect)
        # tạo M codebooks
        # mỗi codebook gồm Ks codewords
        codeword = np.empty((n_subvect, n_cluster, d_subvect), np.float32)
        # print(codeword.shape) = (8, 256, 16)

        for m in range(n_subvect):
            vec_sub = vec[:, m * d_subvect: (m + 1) * d_subvect]
            # thực hiện phân cụm bằng k-means trên từng tập sub-vector thứ m
            centroids, labels = kmeans2(vec_sub, n_cluster)
            # centroids: (Ks x Ds)
            # labels: vec.shape[0]
            codeword[m] = centroids

        return codeword

    def encode(self, codeword, vec):
        n_subvect, n_cluster, d_subvect = codeword.shape
        # tạo pq-code cho n samples (với n = vec.shape[0]) mỗi pq-code gồm M giá trị
        pqcode = np.empty((vec.shape[0], n_subvect), np.uint8)
        for m in range(n_subvect):
            vec_sub = vec[:, m * d_subvect: (m + 1) * d_subvect]
            # codes: 1 mảng gồm n phần tử (n = vec.shape[0]), lưu giữ cluster index gần nhất của sub-vector thứ m của từng vector
            # distances: 1 mảng gồm n phần từ (n = vec.shape[0]), lưu giữ khoảng cách giữa sub-vector thứ m của từng vector với centroid gần nhất
            codes, distances = vq(vec_sub, codeword[m])
            # codes: vec.shape[0]
            # distances: vec.shape[0]
            pqcode[:, m] = codes
        return pqcode


    def search(self, codeword, pqcode, query):
        M, Ks, Ds = codeword.shape
        dist_table = np.empty((M, Ks), np.float32)
        for m in range(M):
            query_sub = query[m * Ds: (m + 1) * Ds]
            dist_table[m, :] = cdist([query_sub], codeword[m], 'cosine')[0]
        dist = np.sum(dist_table[range(M), pqcode], axis=1)
        return dist


if __name__ == '__main__':
    pq = PQ()
    codeword = pq.train(feature, 8)
    pqcode = pq.encode(codeword, feature)
    np.savez_compressed(root_feature_path+"feature_pq", array1=codeword, array2=pqcode)