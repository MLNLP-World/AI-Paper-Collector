import datetime
import json
import os
import re

import pytz
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

cn = pytz.timezone("Asia/Shanghai")

app = Flask(__name__)
boo = Bootstrap(app)

template_folder = "templates"
# Templates Acknowledge: https://github.com/ronaldosvieira/simple-search-template
# LICENCE: MIT

app.config["TEMPLATES_AUTO_RELOAD"] = True

base_dir = os.path.dirname(os.path.abspath(__file__))

cache_json = os.path.join(base_dir, "cache", "cache.json")
cache_data = {}
support_confs = []


def add_item(item: dict):
    # print(item)
    if item["conf"] not in cache_data.keys():
        cache_data[item["conf"]] = {}
    if item["year"] not in cache_data[item["conf"]].keys():
        cache_data[item["conf"]][item["year"]] = []
    cache_data[item["conf"]][item["year"]].append(
        {"title": item["title"], "title_format": item["title_format"]}
    )


def load_data():
    with open(cache_json, "r") as f:
        data = json.load(f)

    for conf in data:
        year = re.search(r"\d{4}", conf).group()
        # cut by year
        conf_name = re.sub(r"\d{4}(.*)", "", conf).strip()
        if conf_name.upper() not in support_confs:
            support_confs.append(conf_name.upper())

        for paper in data[conf]:
            # print(conf_name, year, paper)
            add_item(
                {
                    "conf": conf_name.upper(),
                    "year": year,
                    "title": paper,
                    "title_format": re.sub("-", " ", re.sub(r"\s+", " ", paper)).lower(),
                }
            )

    support_confs.sort()


def prepare():
    load_data()


prepare()


def search(query, confs, year):
    # search in database
    results = {}
    for conf in confs:
        conf_results = {}
        for conf_year in cache_data[conf].keys():
            if year is not None and int(conf_year) < year:
                continue
            conf_results[conf_year] = []
            for paper in cache_data[conf][conf_year]:
                if query in paper["title_format"]:
                    conf_results[conf_year].append(paper["title"])
        results[conf.upper()] = conf_results
    return results


@app.route("/")
def index():
    return render_template(
        "index.html", confs=support_confs, year_now=datetime.datetime.now(cn).year
    )


@app.route("/r", methods=["POST"])
def result():
    query = request.form.get("query") or None
    if query is None:
        return render_template(
            "index.html", confs=support_confs, year_now=datetime.datetime.now(cn).year
        )
    else:
        last_query = query
        query = query.strip().lower()
        query = re.sub("-", " ", re.sub(r"\s+", " ", query))

    year = request.form.get("year") or None
    if year is not None:
        year = int(year)
    else:
        year = 2000

    confs = request.form.getlist("confs") or None
    if confs is not None:
        confs = [x.upper() for x in confs]
        confs = [x for x in confs if x in support_confs]

    print(query, confs, year)
    results = search(query, confs, year)
    print(results)
    return render_template(
        "result.html",
        confs=support_confs,
        last_query=last_query,
        year_now=datetime.datetime.now(cn).year,
        json_data=json.dumps(results),
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=False)
