import pytest

import numpy as np

from kmeans import KMeans


def test_kmeans_inits():
    kmeans = KMeans(n_clusters=4, max_iter=150, tol=1e-5)

    assert kmeans.n_clusters == 4
    assert kmeans.max_iter == 150
    assert kmeans.tol == 1e-5


def test_kmeans_results():
    X = np.array([
        [-10.85671346,  10.4892844 ],
        [ -5.57438678,   4.67884414],
        [ -4.09293858,   1.20212053],
        [ -5.26210402,   0.63557869],
        [ -9.6730844 ,   7.6969948 ],
        [-12.85591727,   8.91007606],
        [ -6.16360032,   3.26627259],
        [ -6.91161607,   4.68076626],
        [ -5.90422768,   3.88712478],
        [ -6.41545621,  -1.11330638],
        [ -4.98760377,   0.74803994],
        [ -6.41487085,   4.93984011],
        [-10.28038181,   8.26907785],
        [ -9.82342069,  10.61675796],
        [ -5.88805993,  -1.53854561],
        [ -4.51872375,   0.29042907],
        [ -8.37266941,   8.69360545],
        [ -7.94627336,   6.01079038],
        [ -7.51456607,   5.27345092],
        [ -9.47601031,   9.24255211],
        [-10.046096  ,   7.78967188],
        [ -6.95223464,   0.02735709],
        [ -5.73090353,  -0.03906842],
        [ -5.82078703,   3.58582513],
        [ -7.72372503,   7.67281333]
        ])
    test_centroids = np.array([
        [-9.90089093,  8.82009265],
        [-5.48100305,  0.02657561],
        [-6.53129102,  4.54036429]
        ])
    test_clusters = np.array([
        0, 2, 1, 1, 0, 0, 2, 2, 2,
        1, 1, 2, 0, 0, 1, 1, 0, 2,
        2, 0, 0, 1, 1, 2, 0
        ])

    kmeans = KMeans(n_clusters=3, tol=1e-6, random_state=90210)
    kmeans.fit(X)

    assert np.allclose(test_centroids, kmeans.centroids)
    assert np.allclose(test_clusters, kmeans.predict(X))


def test_kmeans_methods():
    X = np.array([
        [-10.85671346,  10.4892844 ],
        [ -5.57438678,   4.67884414],
        [ -4.09293858,   1.20212053],
        [ -5.26210402,   0.63557869],
        [ -9.6730844 ,   7.6969948 ],
        [-12.85591727,   8.91007606],
        [ -6.16360032,   3.26627259],
        [ -6.91161607,   4.68076626],
        [ -5.90422768,   3.88712478],
        [ -6.41545621,  -1.11330638],
        [ -4.98760377,   0.74803994],
        [ -6.41487085,   4.93984011],
        [-10.28038181,   8.26907785],
        [ -9.82342069,  10.61675796],
        [ -5.88805993,  -1.53854561],
        [ -4.51872375,   0.29042907],
        [ -8.37266941,   8.69360545],
        [ -7.94627336,   6.01079038],
        [ -7.51456607,   5.27345092],
        [ -9.47601031,   9.24255211],
        [-10.046096  ,   7.78967188],
        [ -6.95223464,   0.02735709],
        [ -5.73090353,  -0.03906842],
        [ -5.82078703,   3.58582513],
        [ -7.72372503,   7.67281333]
        ])

    kmeans = KMeans(n_clusters=3, tol=1e-6, random_state=90210)
    kmeans.fit(X)

    kmeans2 = KMeans(n_clusters=3, tol=1e-6, random_state=90210)

    assert np.allclose(kmeans.predict(X), kmeans2.fit_predict(X))
