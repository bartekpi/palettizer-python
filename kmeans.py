from copy import deepcopy
import numpy as np


class KMeans():

    def __init__(self, n_clusters=2, max_iter=200,
                 random_state=None, tol=1e-4):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.random_state = random_state
        self.tol = tol
        np.random.seed(self.random_state)

    def fit(self, X):
        n_dims = X.shape[1]
        self.centroids = np.zeros((self.n_clusters, n_dims))
        clusters = np.zeros(X.shape[0])

        value_range = X.min()//2, X.max()//2
        for i in range(self.n_clusters):
            self.centroids[i, :] = np.random.uniform(
                *value_range, n_dims)

        for k in range(self.max_iter):
            clusters = self.predict(X)

            new_centroids = np.random.uniform(
                *value_range, (self.n_clusters, n_dims))

            for i in range(self.n_clusters):
                X_slice = X[clusters == i]
                if X_slice.shape[0] > 0:
                    new_centroids[i] = np.nanmean(X_slice, axis=0)

            last_distance = np.linalg.norm(
                new_centroids - self.centroids, axis=1).sum()
            self.centroids = deepcopy(new_centroids)

            if last_distance < self.tol:
                break

    def predict(self, X):
        clusters = np.argmin(
            np.stack([np.linalg.norm(self.centroids[i] - X, axis=1)
                      for i in range(self.n_clusters)
                     ], axis=1), axis=1)

        return clusters

    def fit_predict(self, X):
        self.fit(X)

        return self.predict(X)
