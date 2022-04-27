from unittest import result
from flask import Flask, render_template, request, make_response
from flask_bootstrap import Bootstrap
import os
import pytz
from constant import init
from searcher import exec_search

cn = pytz.timezone('Asia/Shanghai')

app = Flask(__name__)
bootstrap = Bootstrap(app)

template_folder = 'templates'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['UPLOAD_FOLDER'] = 'static/images'

base_dir = os.path.dirname(os.path.abspath(__file__))

indexes, candidates = init()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/r', methods=['GET'])
def result():
    mode = request.args.get('mode') or 'fuzzy'
    threshold = request.args.get('threshold') or 50
    limit = request.args.get('limit') or None
    confs = request.args.get('confs') or None
    query = request.args.get('query') or None

    print(mode, threshold, limit, confs, query)

    results = exec_search(indexes, candidates, query, mode, threshold, confs, limit)
    return render_template('result.html', results=results)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
