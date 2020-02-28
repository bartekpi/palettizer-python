from collections import Counter
from io import BytesIO
import base64

from PIL import Image, ImageDraw
import numpy as np

from kmeans import KMeans


def rgb2hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*[int(x) for x in rgb])


def receive_image(buf):
    return Image.open(BytesIO(buf))


def image_to_array(img, img_size):
    denom = np.sqrt(np.product(img.size[:2]) / img_size**2)
    im = np.asarray(img.resize(
        (np.array(img.size) / denom).astype(int)), dtype='int32')
    X = im.reshape((im.shape[0]*im.shape[1], 3))

    return X, im.shape


def image_resize(img, img_size):
    denom = np.sqrt(max(1, np.product(img.size[:2]) / img_size**2))
    im = np.asarray(img.resize(
        (np.array(img.size) / denom).astype(int)), dtype='int32')

    img = img.resize((np.array(img.size) / denom).astype(int))
    buf = BytesIO()
    img.save(buf, format='jpeg')

    return base64.b64encode(buf.getvalue()).decode('utf')


def get_clusters(X, algo, n_clusters):
    if algo == 'KMeans':
        clf = KMeans(n_clusters=n_clusters)
    else:
        clf = KMeans(n_clusters=n_clusters)

    clf.fit(X)

    return clf


def get_colors_from_clf(clf, X):
    clf_labels = clf.predict(X)

    colors = []
    hist = []
    items = sorted(Counter(clf_labels).items())
    for k, v in items:
        colors.append(X[clf_labels == k].mean(axis=0).astype(int).tolist())
        hist.append(v)

    return hist, colors


def get_image_from_clf(clf, colors, X, dims):
    recoded = np.array([
        [int(y) for y in colors[x]]
        for x in clf.predict(X)]).reshape(dims)

    buf = BytesIO()
    Image.fromarray(np.uint8(recoded)).save(buf, format='jpeg')

    return base64.b64encode(buf.getvalue()).decode('utf')


def generate_image(w, h, color):
    img_io = BytesIO()
    Image.new('RGB', (w, h), color).save(img_io, 'JPEG', quality=90)
    img_io.seek(0)
    return img_io
