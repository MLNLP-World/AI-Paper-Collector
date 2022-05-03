import shutil
from flask import Flask, render_template, request, make_response
from flask_bootstrap import Bootstrap
import os
import pytz
import datetime
import time
import json
import sqlite3
import re

cn = pytz.timezone('Asia/Shanghai')

app = Flask(__name__)
boo = Bootstrap(app)

template_folder = 'templates'
# Templates Acknowledge: https://github.com/ronaldosvieira/simple-search-template
# LICENCE: MIT

app.config['TEMPLATES_AUTO_RELOAD'] = True

base_dir = os.path.dirname(os.path.abspath(__file__))

db_conn = None
db_path = os.path.join(base_dir, 'cache', 'data.db')

cache_json = os.path.join(base_dir, 'cache', 'cache.json')
support_confs = []


def init_db():
    if os.path.exists(db_path):
        os.remove(db_path)
        print('Remove old database')
    global db_conn
    db_conn = sqlite3.connect(db_path, check_same_thread=False)
    cur = db_conn.cursor()
    cur.execute(
        'create table papers (conf text, year integer, title text, title_format text, url text, primary key(conf, year, title))'
    )
    db_conn.commit()
    cur.close()


def json2db():
    with open(cache_json, 'r') as f:
        data = json.load(f)

    cur = db_conn.cursor()
    for conf in data:
        year = re.search(r'\d{4}', conf).group()
        # cut by year
        conf_name = re.sub(r'\d{4}(.*)', '', conf).strip()
        if conf_name.upper() not in support_confs:
            support_confs.append(conf_name.upper())

        for paper in data[conf]:
            # print(conf_name, year, paper)
            cur.execute(
                'insert or ignore into papers values (?, ?, ?, ?, ?)',
                (conf_name, int(year), paper, re.sub('-', ' ', re.sub(r'\s+', ' ', paper)), ''))
        db_conn.commit()
    cur.close()

    support_confs.sort()


def prepare():
    init_db()
    json2db()


prepare()


def search(query, confs, year, limit=None):
    # search in database
    cur = db_conn.cursor()
    results = {}
    for conf in confs:
        conf_results = {}
        for row in cur.execute(
                'select year, title from papers where conf=? and year>=? and title_format like ? order by year desc',
            (conf, year, '%' + query + '%')):
            if year not in conf_results.keys():
                conf_results[row[0]] = []
            conf_results[row[0]].append(row[1])
        results[conf.upper()] = conf_results
    cur.close()
    return results


@app.route('/')
def index():
    return render_template('index.html',
                           confs=support_confs,
                           year_now=datetime.datetime.now(cn).year)


@app.route('/r', methods=['POST'])
def result():
    query = request.form.get('query') or None
    if query is None:
        return render_template('index.html',
                               confs=support_confs,
                               year_now=datetime.datetime.now(cn).year)

    # mode = request.form.get('mode') or 'exact'
    # if mode not in ['fuzzy', 'exact']:
    #     mode = 'exact'

    # limit = request.form.get('limit') or None
    # if limit is None or (type(limit) is str and limit.isdigit() is False):
    #     limit = None
    # else:
    #     limit = int(limit)

    # threshold = request.form.get('threshold') or 50
    # if threshold is None or (type(threshold) is str and threshold.isdigit() is False):
    #     threshold = 50
    # else:
    #     threshold = int(threshold)

    year = request.form.get('year') or None
    if year is not None:
        year = int(year)
    else:
        year = 0

    confs = request.form.getlist('confs') or None
    if confs is not None:
        confs = [x.upper() for x in confs]
        confs = [x for x in confs if x in support_confs]

    # print(query, confs, year)
    results = search(query, confs, year, None)
    # print(results)
    return render_template('result.html',
                           results=results,
                           confs=support_confs,
                           year_now=datetime.datetime.now(cn).year)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
