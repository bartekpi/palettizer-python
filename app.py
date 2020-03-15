from flask import Flask, render_template, request, flash, send_file

from config import (
    FLASK_SECRET_KEY, APP_NAME, APP_TITLE, APP_REPO,
    N_CLUSTERS, ALLOWED_EXTENSIONS)

from funcs import (
    receive_image, generate_image, image_to_array, get_clusters,
    get_colors_from_clf, image_resize, get_image_from_clf, rgb2hex
    )

app = Flask(__name__, static_url_path=f'/{APP_NAME}/static')
app.secret_key = FLASK_SECRET_KEY


@app.route(f'/{APP_NAME}/', methods=['GET', 'POST'], strict_slashes=False)
def index():
    context = dict(app_name=APP_NAME, app_title=APP_TITLE, app_repo=APP_REPO)
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
