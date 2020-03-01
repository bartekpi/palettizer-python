from flask import Flask, render_template, request, flash, send_file

from config import FLASK_SECRET_KEY, N_CLUSTERS, ALLOWED_EXTENSIONS
from funcs import (
    receive_image, generate_image, image_to_array, get_clusters,
    get_colors_from_clf, image_resize, get_image_from_clf, rgb2hex
    )

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY
app_name = 'pltzr-python'

@app.route(f'/{app_name}/image', methods=['GET'])
def get_image():
    parms = {}
    for arg in 'whrgb':
        try:
            parms[arg] = int(request.args[arg])
        except:
            return generate_image(100, 100, '#ff0000')

    for arg in 'wh':
        parms[arg] = max(25, min(250, parms[arg]))

    for arg in 'rgb':
        parms[arg] = max(0, min(255, parms[arg]))

    color = (parms['r'], parms['g'], parms['b'])

    image = generate_image(parms['w'], parms['h'], color)
    return send_file(image, mimetype='image/jpeg')


@app.route(f'/{app_name}', methods=['GET', 'POST'], strict_slashes=False)
def index():
    context = {}
    if request.method == 'POST':
        if request.form['action'] == 'upload':
            file_in = request.files['customFile']
            file_in_extension = file_in.filename.split('.')[-1].lower()
            if file_in_extension not in ALLOWED_EXTENSIONS:
                flash('File type not allowed')
                return render_template('index.html', **context)

            try:
                n_clusters = min(16, max(4, int(request.form.get(
                                        'customNClusters', N_CLUSTERS))))
            except ValueError:
                n_clusters = N_CLUSTERS

            # clustering_algo = request.form.get('customClusteringAlgo')
            clustering_algo = 'KMeans'

            img = receive_image(file_in.read())

            X_train, dims_train = image_to_array(img, 96)
            X_apply, dims_apply = image_to_array(img, 384)

            # calculate clusters
            clf = get_clusters(X_train, clustering_algo, n_clusters)
            hist, colors = get_colors_from_clf(clf, X_train)

            # output data
            context['image_pre'] = image_resize(img, 384)
            context['image_post'] = (
                get_image_from_clf(clf, colors, X_apply, dims_apply))
            context['image_width'] = dims_apply[1]
            context['thumbnail_width'] = int(
                round(dims_apply[1] / n_clusters, 0))
            context['thumbnail_height'] = 64

            hist, colors = zip(*sorted(zip(hist, colors),
                                       key=lambda x: x[0],
                                       reverse=True)
                                       )
            hist_sum = sum(hist)
            hist_norm = [int(round(dims_apply[1] * x/hist_sum, 0))
                         for x in hist]
            hist_norm = [int(round(dims_apply[1]/n_clusters, 0))
                         for x in range(n_clusters)]
            colors_hex = [rgb2hex(x) for x in colors]
            context['colors'] = list(zip(colors_hex, colors, hist_norm))

            context['processed'] = True


    context['max_width'] = context.get('image_width', 512)

    return render_template('index.html', **context)
