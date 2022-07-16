import json
import os
import re

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def search_from_iclr(url, name, res):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
    }
    r = requests.get(url, headers=headers)
    data = r.json()
    if name not in res:
        res[name] = []
    for item in data["notes"]:
        res[name].append(
            {
                "paper_name": item["content"]["title"], 
                "paper_url": "https://openreview.net" + item["content"]["pdf"],
                "paper_authors": item["content"]["authors"],
                "paper_abstract": item['content']['abstract'],
            }
        )
    return res


def search_from_nips(url, name, res):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    if name not in res:
        res[name] = []
    url_prefix = "https://" + url[8:].split("/")[0]
    for paper_item in soup.find(class_="col").ul.find_all("li"):
        paper_url = url_prefix + paper_item.a["href"]
        res[name].append(
            {
                "paper_name": paper_item.a.string, 
                "paper_url": paper_url,
                "paper_authors": [author.strip() for author in paper_item.i.string.split(',')],
                "paper_abstract": "",
            }
        )
    return res


def search_from_acl(url, tag, name, res):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    if name not in res:
        res[name] = []
    for tp in soup.find_all("p", class_="d-sm-flex align-items-stretch"):
        cls = tp.find("strong")
        for paper_item in cls.find_all(href=re.compile(tag), class_="align-middle"):
            items = [item.string if item.string else item for item in paper_item.contents]

            paper = "".join([item for item in items if isinstance(item, str)])
            paper_url = "https://aclanthology.org" + paper_item["href"]
            if tp.next_sibling is not None and tp.next_sibling.string is not None:
                paper_abstract = tp.next_sibling.string
            else:
                paper_abstract = ""
            
            res[name].append(
                {
                    "paper_name": paper,
                    "paper_url": paper_url,
                    "paper_authors": [author.string for author in tp.find_all('a', href=re.compile("people/"))],
                    "paper_abstract": paper_abstract,
                }
            )
    return res


def search_from_dblp(url, name, res):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    if name not in res:
        res[name] = []

    for paper_item in soup.find_all("li", class_="entry"):
        paper_url = paper_item.find("li", class_="drop-down").div.a["href"]
        paper_name = paper_item.find(class_="title", itemprop="name")
        paper_authors = [
            re.sub('\d', '', author['title']).strip() for author in paper_item.find_all(class_=None, itemprop="name")]
        items = [item.string if item.string else item for item in paper_name.contents]
        paper = "".join([item for item in items if isinstance(item, str)])
        res[name].append(
            {
                "paper_name": paper, 
                "paper_url": paper_url,
                "paper_authors": paper_authors,
                "paper_abstract": "",
            }
        )
    return res


def search_from_thecvf(url, name, res):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    if name not in res:
        res[name] = []
        
    for paper_item in soup.find_all("dt", class_="ptitle"):
        paper_url = "https://openaccess.thecvf.com" + paper_item.a["href"]
        paper = paper_item.a.string
        paper_authors = [author.string for author in paper_item.next_sibling.next_sibling.find_all('a', href='#')]
        res[name].append(
            {
                "paper_name": paper, 
                "paper_url": paper_url,
                "paper_authors": paper_authors,
                "paper_abstract": "",
            }
        )
    return res


def crawl(cache_file=None, force=False):
    res = {}

    acl_conf = json.load(open("conf/acl_conf.json", "r"))
    dblp_conf = json.load(open("conf/dblp_conf.json", "r"))
    nips_conf = json.load(open("conf/nips_conf.json", "r"))
    iclr_conf = json.load(open("conf/iclr_conf.json", "r"))
    thecvf_conf = json.load(open("conf/thecvf_conf.json", "r"))

    cache_conf = []
    cache_res = {}
    if not force and cache_file is not None and os.path.exists(cache_file):
        # incremental update
        cache_res = json.load(open(cache_file, "r"))
        cache_conf = [name for name in cache_res.keys()]

    for conf in tqdm(acl_conf, desc="[+] Crawling ACL", dynamic_ncols=True):
        assert conf.get("name") and conf.get("url") and conf.get("tag")
        url, tag, name = conf["url"], conf["tag"], conf["name"]
        if name in cache_conf:
            continue
        res = search_from_acl(url, tag, name, res)

    for conf in tqdm(dblp_conf, desc="[+] Crawling DBLP", dynamic_ncols=True):
        assert conf.get("name") and conf.get("url")
        url, name = conf["url"], conf["name"]
        if name in cache_conf:
            continue
        res = search_from_dblp(url, name, res)

    for conf in tqdm(nips_conf, desc="[+] Crawling NeurIPS", dynamic_ncols=True):
        assert conf.get("name") and conf.get("url")
        url, name = conf["url"], conf["name"]
        if name in cache_conf:
            continue
        res = search_from_nips(url, name, res)

    for conf in tqdm(iclr_conf, desc="[+] Crawling ICLR", dynamic_ncols=True):
        assert conf.get("name") and conf.get("url")
        url, name = conf["url"], conf["name"]
        if name in cache_conf:
            continue
        res = search_from_iclr(url, name, res)

    for conf in tqdm(thecvf_conf, desc="[+] Crawling openacess.thecvf", dynamic_ncols=True):
        assert conf.get("name") and conf.get("url")
        url, name = conf["url"], conf["name"]
        if name in cache_conf:
            continue
        res = search_from_thecvf(url, name, res)

    res.update(cache_res)
    return res


def do_crawl(cache_file=None, force=False):
    if force or cache_file is None or not os.path.exists(cache_file):
        print(f"[+] Crawling papers...")
        res = crawl(cache_file)
        with open(cache_file, "w") as f:
            json.dump(res, f)
    else:
        print(f"[+] Loading from cache...")
        with open(cache_file, "r") as f:
            res = json.load(f)
    return res


if __name__ == "__main__":
    do_crawl(cache_file="cache/cache.json", force=True)
