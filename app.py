from flask import Flask, render_template, request, make_response
from flask_bootstrap import Bootstrap
import os
import pytz
import datetime
import json
import re

cn = pytz.timezone("Asia/Shanghai")

app = Flask(__name__)
boo = Bootstrap(app)

template_folder = "templates"
# Templates Acknowledge: https://github.com/ronaldosvieira/simple-search-template
# LICENCE: MIT

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["CACHE_TYPE"] = "null"
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

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
        {
            "title": item["title"], 
            "title_format": item["title_format"],
            "url": item["url"],
            "authors": item["authors"],
            "abstract": item["abstract"],
            "code": item["code"],
            "citation": item["citation"],
        }
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
            add_item(
                {
                    "conf": conf_name.upper(),
                    "year": year,
                    "title": paper["paper_name"],
                    "title_format": re.sub("-", " ", re.sub("\s+", " ", paper["paper_name"])).lower(),
                    "url": paper["paper_url"],
                    "authors": paper["paper_authors"],
                    "abstract": paper["paper_abstract"],
                    "code": paper["paper_code"],
                    "citation": paper["paper_cite"],
                }
            )

    support_confs.sort()


def prepare():
    load_data()


prepare()



def search(query, confs, year, sp_year=None, sp_author=None, limit=None):

    def match_author(authors, sp_author):
        if sp_author is None:
            return True
        authors = [author.lower().replace("-"," ") for author in authors]
        author_format = " ".join(authors)
        if len(sp_author.split(" ")) > 1:
            return sp_author.lower() in authors
        else:
            return sp_author.lower() in author_format

    # search in database
    result_count = 0
    results = {}
    for conf in confs:
        conf_results = {}
        if conf not in cache_data.keys():
            continue
        for conf_year in cache_data[conf].keys():
            if sp_year is not None and int(conf_year) != sp_year:
                continue
            if sp_year is None and year is not None and int(conf_year) < year:
                continue
            conf_results[conf_year] = []
            for paper in cache_data[conf][conf_year]:
                if not match_author(paper["authors"], sp_author):
                    continue
                if query.lower() == 'findall' and len(confs) == 1:
                    conf_results[conf_year].append({
                        "title": paper["title"], 
                        "url": paper["url"],
                        "authors": paper["authors"],
                        "abstract": paper["abstract"],
                        "code": paper["code"],
                        "citation": paper["citation"],
                    })
                    result_count += 1
                    if limit is not None and result_count >= limit:
                        break
                elif query in paper["title_format"]:
                    conf_results[conf_year].append({
                        "title": paper["title"], 
                        "url": paper["url"],
                        "authors": paper["authors"],
                        "abstract": paper["abstract"],
                        "code": paper["code"],
                        "citation": paper["citation"],
                    })
                    result_count += 1
                    if limit is not None and result_count >= limit:
                        break
                elif query == "#":
                    conf_results[conf_year].append({
                        "title": paper["title"], 
                        "url": paper["url"],
                        "authors": paper["authors"],
                        "abstract": paper["abstract"],
                        "code": paper["code"],
                        "citation": paper["citation"],
                    })
                    result_count += 1
                    if limit is not None and result_count >= limit:
                        break
            if limit is not None and result_count >= limit:
                break
        if limit is not None and result_count >= limit:
            break
        results[conf.upper()] = conf_results
    return results


@app.route("/")
def index():
    return render_template("index.html", confs=support_confs, year_now=datetime.datetime.now(cn).year)


@app.route("/r", methods=["POST", "GET"])
def result():
    query = request.form.get("query") or request.args.get("query") or None
    year = request.form.get("year") or request.args.get("year") or None
    sp_year = request.form.get("sp_year") or request.args.get("sp_year") or None
    sp_author = request.form.get("sp_author") or request.args.get("sp_author") or None
    confs = request.form.getlist("confs") or request.args.getlist("confs") or None
    searchtype = request.form.get("searchtype") or request.args.get("searchtype") or None

    if query is None and sp_author is None:
        return render_template("index.html", confs=support_confs, year_now=datetime.datetime.now(cn).year)
    elif searchtype == 'author':
        sp_author = query
        last_query = "#"
        query = "#"      
    elif query is None and sp_author is not None:
        last_query = "#"
        query = "#"
    else:
        last_query = query
        query = query.strip().lower()
        query = re.sub("-", " ", re.sub("\s+", " ", query))

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

    
    if year is not None:
        year = int(year)
    else:
        year = 2000

    
    if sp_year is not None:
        sp_year = int(sp_year)

    
    if sp_author is not None:
        sp_author = sp_author.strip().lower()
        sp_author = re.sub("-", " ", re.sub("\s+", " ", sp_author))

    
    if confs is not None:
        confs = [x.upper() for x in confs]
        confs = [x for x in confs if x in support_confs]


    results = search(query, confs, year, sp_year=sp_year, sp_author=sp_author, limit=5000)
    return render_template(
        "result.html",
        confs=support_confs,
        last_query=last_query,
        year_now=datetime.datetime.now(cn).year,
        json_data=json.dumps(results),
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000, use_reloader=True)
