from flask import Flask, render_template, request, make_response, jsonify
from flask_bootstrap import Bootstrap
import os
import pytz
import datetime
import json
import re
import time
import asyncio
import openai
from EdgeGPT import Chatbot as ChatbotEdge
from revChatGPT.Official import Chatbot as ChatbotOfficial

app = Flask(__name__, static_folder='static', static_url_path="")

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
    


load_data()


def search(query, confs, year, sp_year=None, sp_author=None, limit=None):
    def match_author(authors, sp_author):
        if sp_author is None:
            return True
        authors = [author.lower().replace("-", " ") for author in authors]
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
            conf_results_per_year = []
            for paper in cache_data[conf][conf_year]:
                if not match_author(paper["authors"], sp_author):
                    continue
                if query.lower() == 'findall' and len(confs) == 1:
                    conf_results_per_year.append({
                        "year": conf_year,
                        "conf": conf,
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
                    conf_results_per_year.append({
                        "year": conf_year,
                        "conf": conf,
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
                    conf_results_per_year.append({
                        "year": conf_year,
                        "conf": conf,
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
                        
            if len(conf_results_per_year) != 0:
                conf_results[conf_year] = conf_results_per_year
                
            if limit is not None and result_count >= limit:
                break
            
        if limit is not None and result_count >= limit:
            break
            
        if len(conf_results) != 0:    
            results[conf.upper()] = conf_results
            
    return results

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route("/api/get_guess_you_like", methods=["POST", "GET"])
def get_guess_you_like_api():
    query = request.form.get("query") or request.args.get("query") or None
    if query is None:
        return {"message:": "query is null."}
    st = time.time()
    try:
        # response  = asyncio.run(askEdgeHelper(query))
        # response = askChatHelper(query)
        response = askChatGPTAPI(query)
    except:
        response = {"message": "Sorry, the sevice is not available now. Please hold on."}
    ed = time.time()
    response['timecost'] = str(round(ed - st, 2) * 100) + 'ms'
    # test = {"keywords": ["multimodal", "multimodal learning", "multimodal representation", "multimodal fusion",
    #                      "multimodal interaction", "multimodal analysis", "multimodal classification",
    #                      "multimodal data", "multimodal networks", "multimodal retrieval"], "timecost": "540.0ms"}
    # time.sleep(10)
    data = {"msg": "success", "data": response}
    payload = jsonify(data)
    return payload, 200


def askChatGPTAPI(query):
    engine = "gpt-3.5-turbo"
    temperature = 0.5
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    openai.api_base = os.environ.get("OPENAI_API_BASE")
    prompt = f'Please just return the top-10 related keywords of papers on "{query}" in JSON format with the key named "keywords". The output must start with "```json" and end with "```".'
    response = openai.ChatCompletion.create(
        model=engine,
        messages=[
            {"role": "system", "content": "You are a helpful assistant for search suggestion of paper in the field of artificial intelligence"},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature
    )
    response = response['choices'][0]['message']['content']
    keywords = re.search("```json(.*)```", response, flags=re.DOTALL).group(1)
    keywords = json.loads(keywords)
    return keywords

def askChatHelper(query):
    engine = os.environ.get("OPENAI_ENGINE") or 'text-davinci-003'
    api_key = os.environ.get("OPENAI_API_KEY")
    proxy = os.environ.get("OPENAI_PROXY")
    temperature = 0.5
    prompt = f'If I want to search for papers on "{query}", what keywords are recommended to me? Please just return the top-10 related keywords of papers in JSON format with the key named "keywords". The output must start with "```json" and end with "```".'
    chatbot = ChatbotOfficial(api_key=api_key, engine=engine, proxy=proxy)
    response = chatbot.ask(prompt, temperature=temperature)["choices"][0]["text"]
    keywords = re.search("```json(.*)```", response, flags=re.DOTALL).group(1)
    keywords = json.loads(keywords)
    return keywords


async def askEdgeHelper(query):
    bot = ChatbotEdge()
    prompt = f'Let us talk about search suggestion: If I want to search for papers on "{query}", what related and short search terms are suggested to me, please just return the top-10 related keywords of papers in JSON format. Do not perform any searches. No additional information or search results should be included in the output. The format is ```json``` with the key named "keywords".'
    response = (await bot.ask(prompt=prompt))["item"]["messages"][1]["adaptiveCards"][0]["body"][0]["text"]
    keywords = re.search("```json(.*)```", response, flags=re.DOTALL).group(1)
    keywords = json.loads(keywords)
    await bot.close()
    return keywords


@app.route("/api/search", methods=["POST", "GET"])
def search_api():
    query = request.form.get("query") or request.args.get("query") or None
    year = request.form.get("year") or request.args.get("year") or None
    sp_year = request.form.get("sp_year") or request.args.get("sp_year") or None
    sp_author = request.form.get("sp_author") or request.args.get("sp_author") or None
    confs_string = request.form.get("confs") or request.args.get("confs") or None
    searchtype = request.form.get("searchtype") or request.args.get("searchtype") or None
    confs = confs_string.split(',')
    if searchtype == 'author':
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
    data = {"msg": "success", "data": results}

    payload = jsonify(data)
    return payload, 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001, use_reloader=True)
