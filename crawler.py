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
        res[name].append({
                          "paper_name": item["content"]["title"],
                          'paper_url': 'https://openreview.net'+item["content"]["pdf"]
                          })
    return res


def search_from_nips(url, name, res):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    if name not in res:
        res[name] = []
    for paper_item in soup.find(class_='col').ul.find_all('a'):
        res[name].append({
                          "paper_name": paper_item.string,
                          'paper_url': "https://papers.nips.cc"+paper_item["href"]
                          })
    return res


def search_from_acl(url, tag, name, res):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    if name not in res:
        res[name] = []
    for tp in soup.find_all('p',class_="d-sm-flex align-items-stretch"):
        cls=tp.find('strong')
        for paper_item in cls.find_all(href=re.compile(tag), class_="align-middle"):
            items = [item.string if item.string else item for item in paper_item.contents]
            try:
                paper = "".join([item for item in items if isinstance(item, str)])
                paper_url='https://aclanthology.org'+paper_item['href']
            except:
                import pdb
                pdb.set_trace()
            res[name].append({"paper_name":paper,
                              'paper_url': paper_url,
                              })
    return res


def search_from_dblp(url, name, res):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    if name not in res:
        res[name] = []

    for paper_item in soup.find_all("li", class_='inproceedings'):
        paper_url=paper_item.find("li", class_="drop-down").div.a['href']
        paper_name=paper_item.find(class_='title', itemprop="name")
        items = [item.string if item.string else item for item in paper_name.contents]
        try:
            paper = "".join([item for item in items if isinstance(item, str)])
        except:
            import pdb
            pdb.set_trace()
        res[name].append({"paper_name":paper,
                          'paper_url':paper_url
                          })
    return res


def crawl(cache_file=None):
    res = {}

    acl_conf = json.load(open("conf/acl_conf.json", "r"))
    dblp_conf = json.load(open("conf/dblp_conf.json", "r"))
    nips_conf = json.load(open("conf/nips_conf.json", "r"))
    iclr_conf = json.load(open("conf/iclr_conf.json", "r"))

    cache_conf = []
    cache_res = {}
    if cache_file is not None and os.path.exists(cache_file):
        # incremental update
        cache_res = json.load(open(cache_file, "r"))
        cache_conf = [name for name in cache_res.keys()]

    # for conf in tqdm(acl_conf, desc="[+] Crawling ACL", dynamic_ncols=True):
    #     assert conf.get("name") and conf.get("url") and conf.get("tag")
    #     url, tag, name = conf["url"], conf["tag"], conf["name"]
    #     if name in cache_conf:
    #         continue
    #     res = search_from_acl(url, tag, name, res)
    #
    # for conf in tqdm(dblp_conf, desc="[+] Crawling DBLP", dynamic_ncols=True):
    #     assert conf.get("name") and conf.get("url")
    #     url, name = conf["url"], conf["name"]
    #     if name in cache_conf:
    #         continue
    #     res = search_from_dblp(url, name, res)
    #
    # for conf in tqdm(nips_conf, desc="[+] Crawling NeurIPS", dynamic_ncols=True):
    #     assert conf.get("name") and conf.get("url")
    #     url, name = conf["url"], conf["name"]
    #     if name in cache_conf:
    #         continue
    #     res = search_from_nips(url, name, res)

    for conf in tqdm(iclr_conf, desc="[+] Crawling ICLR", dynamic_ncols=True):
        assert conf.get("name") and conf.get("url")
        url, name = conf["url"], conf["name"]
        if name in cache_conf:
            continue
        res = search_from_iclr(url, name, res)

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
