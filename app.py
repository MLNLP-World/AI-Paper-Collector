from flask import Flask, render_template, request, make_response
from flask_bootstrap import Bootstrap
import os
import pytz
from constant import init
from searcher import exec_search

cn = pytz.timezone('Asia/Shanghai')

app = Flask(__name__)
boo = Bootstrap(app)

template_folder = 'templates'
# Templates Acknowledge: https://github.com/ronaldosvieira/simple-search-template
# LICENCE: MIT

app.config['TEMPLATES_AUTO_RELOAD'] = True

base_dir = os.path.dirname(os.path.abspath(__file__))

indexes, candidates = init()  # show_prompt=False
support_confs = [
    'ACL', 'EMNLP', 'NAACL', 'COLING', 'CVPR', 'ECCV', 'ICCV', 'ACMMM', 'ICLR', 'ICML', 'AAAI',
    'IJCAI', 'SIGIR', 'KDD', 'CIKM', 'WSDM', 'WWW', 'ECIR'
]


@app.route('/')
def index():
    return render_template('index.html', confs=support_confs)


@app.route('/r', methods=['GET'])
def result():
    query = request.args.get('query') or None
    if query is None:
        return render_template('index.html', confs=support_confs)

    mode = request.args.get('mode') or 'fuzzy'
    if mode not in ['fuzzy', 'exact']:
        mode = 'fuzzy'

    limit = request.args.get('limit') or None
    if limit is None or (type(limit) is str and limit.isdigit() is False):
        limit = None
    else:
        limit = int(limit)

    threshold = request.args.get('threshold') or 50
    if threshold is None or (type(threshold) is str and threshold.isdigit() is False):
        threshold = 50
    else:
        threshold = int(threshold)

    confs = request.args.getlist('confs') or None
    if confs is not None:
        confs = [x.upper() for x in confs]
        confs = [x for x in confs if x in support_confs]
        confs = ','.join(confs)

    print(
        f'[+] Searching with query: {query}, mode: {mode}, limit: {limit}, threshold: {threshold}, confs: {confs}'
    )

    results = exec_search(indexes, candidates, query, mode, threshold, confs, limit)
    return render_template('result.html', results=results)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
