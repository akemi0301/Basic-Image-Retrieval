import numpy as np
import pandas as pd
from sklearn.cluster import SpectralClustering

# load features
root_feature_path = "./static/feature/all_features.npz"
data = np.load(root_feature_path)

print(len(data["imgs_feature"]))
print(data["imgs_feature"].shape)

df = pd.DataFrame(data["imgs_feature"])
df['label'] = data["class_imgs"]
df['img_path'] = data["paths_feature"]

print(df.describe(include="all"))

#phan cum features bang thuat toan spectral clustering
spec_cl = SpectralClustering(
    n_clusters=40, 
    n_neighbors=8,
    random_state=25,
    assign_labels='kmeans',
    affinity='nearest_neighbors'
)

cluster = spec_cl.fit_predict(df[df.columns[0:2048]])
df['cluster'] = pd.Series(cluster, index=df.index)
# print(df["cluster"])
Centroids = df.groupby(["cluster"]).mean()
# print(Centroids)

# labels = df[['label', 'cluster']].groupby(['label']).agg(num_cluster = ('cluster' , 'count'), name_cluster = ('cluster' ,  'unique'))

# #save data
df.to_csv("./static/cluster/clusters_40.csv", index = False)
Centroids.to_csv("./static/cluster/centroids_40.csv", index = False)
