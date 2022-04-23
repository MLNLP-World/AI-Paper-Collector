import re
import os
import json
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

def search_from_acl(url, tag, name, res):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    if name not in res:
        res[name] = []
    for cls in soup.find_all('strong'):
        for paper_item in cls.find_all(href=re.compile(tag), class_="align-middle"):
            items = [item.string if item.string else item for item in paper_item.contents]
            try:
                paper = "".join([item for item in items if isinstance(item, str)])
            except:
                import pdb
                pdb.set_trace()
            res[name].append(paper)
    return res

def search_from_dblp(url, name, res):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    if name not in res:
        res[name] = []
    for paper_item in soup.find_all(class_='title', itemprop="name"):
        items = [item.string if item.string else item for item in paper_item.contents]
        try:
            paper = "".join([item for item in items if isinstance(item, str)])
        except:
            import pdb
            pdb.set_trace()
        res[name].append(paper)
    return res


def crawl():
    res = {}

    acl_conf = json.load(open('conf/acl_conf.json', 'r'))
    dblp_conf = json.load(open('conf/dblp_conf.json', 'r'))
    
    for conf in tqdm(acl_conf, desc="[+] Crawling ACL", dynamic_ncols=True):
        url, tag, name = conf['url'], conf['tag'], conf['name']
        res = search_from_acl(url, tag, name, res)

    for conf in tqdm(dblp_conf, desc="[+] Crawling DBLP", dynamic_ncols=True):
        url, name = conf['url'], conf['name']
        res = search_from_dblp(url, name, res)

    return res

def do_crawl(cache_file=None):
    if cache_file is None or not os.path.exists(cache_file):
        print(f'[+] Crawling papers when no cache...')
        res = crawl()
        with open(cache_file, 'w') as f:
            json.dump(res, f)
    else:
        print(f'[+] Loading from cache...')
        with open(cache_file, 'r') as f:
            res = json.load(f)
    return res
    