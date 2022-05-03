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

cache_json = os.path.join(base_dir, 'cache', 'cache.json')
cache_data = {}
support_confs = []


def add_item(item: dict):
    # print(item)
    if item['conf'] not in cache_data.keys():
        cache_data[item['conf']] = {}
    if item['year'] not in cache_data[item['conf']].keys():
        cache_data[item['conf']][item['year']] = []
    cache_data[item['conf']][item['year']].append({
        'title': item['title'],
        'title_format': item['title_format']
    })


def load_data():
    with open(cache_json, 'r') as f:
        data = json.load(f)

    for conf in data:
        year = re.search(r'\d{4}', conf).group()
        # cut by year
        conf_name = re.sub(r'\d{4}(.*)', '', conf).strip()
        if conf_name.upper() not in support_confs:
            support_confs.append(conf_name.upper())

        for paper in data[conf]:
            # print(conf_name, year, paper)
            add_item({
                'conf': conf_name.upper(),
                'year': year,
                'title': paper,
                'title_format': re.sub('-', ' ', re.sub('\s+', ' ', paper)).lower()
            })

    support_confs.sort()


def prepare():
    load_data()
    # print(cache_data)


prepare()


def search(query, confs, year, limit=None):
    # search in database
    results = {}
    for conf in confs:
        conf_results = {}
        for year in range(int(year), datetime.datetime.now(cn).year + 1):
            if str(year) not in cache_data[conf].keys():
                continue
            if year not in conf_results.keys():
                conf_results[year] = []
            for paper in cache_data[conf][str(year)]:
                if query in paper['title_format']:
                    conf_results[year].append(paper['title'])
        results[conf.upper()] = conf_results
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
    else:
        query = query.strip().lower()

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
        year = 2000

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
