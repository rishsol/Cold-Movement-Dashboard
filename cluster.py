import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

dataset = pd.read_csv('clean_finished.csv')
X = dataset.iloc[:, [0, 2]].values #acc
Y = dataset.iloc[:, [4, -1]].values #gyro

from sklearn.cluster import KMeans
wcss = []
for i in range(1, 11) :
  kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = 42)
  kmeans.fit(X)
  wcss.append(kmeans.inertia_)

kmeans = KMeans(n_clusters = 2, init = 'k-means++', random_state = 42)
y_kmeans = kmeans.fit_predict(X)

plt.scatter(X[y_kmeans == 0, 0], X[y_kmeans == 0, 1], s = 100, c = 'red', label = 'cluster 1')
plt.scatter(X[y_kmeans == 1, 0], X[y_kmeans == 1, 1], s = 100, c = 'blue', label = 'cluster 2')
plt.scatter(kmeans.cluster_centers_[:, 0],  kmeans.cluster_centers_[:, 1], s = 100, c= 'yellow', label = 'centroide')
plt.title('Clusters of Acceleration data')
plt.xlabel('x')
plt.ylabel('y')
plt.show()