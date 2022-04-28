import logging
import re
import os
import json
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

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
    # print("DEBUG INFO: search" ,url)
    soup = BeautifulSoup(r.text, 'html.parser')
    if name not in res:
        res[name] = []
    for tp in soup.find_all('p',class_="d-sm-flex align-items-stretch"):
        span_list=tp.find_all('span')
        a_list=span_list[0].find_all('a')
        paper_pdf_str=a_list[0]['href']
        # paper_code = a_list[-1]
        # if(paper_code['title'] is not None and paper_code['title']=='Code'):
        #     paper_code_str=paper_code['href']
        # else:
        #     paper_code_str=None
        cls=tp.find('strong')
        # print('DEBUG INFO: '+str(tp.find_all('strong')[0]))
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
                              "paper_pdf": paper_pdf_str,
                              })
    #         "paper_code": paper_code_str
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

    acl_conf = json.load(open('conf/acl_conf.json', 'r'))
    dblp_conf = json.load(open('conf/dblp_conf.json', 'r'))
    nips_conf = json.load(open('conf/nips_conf.json', 'r'))

    cache_conf = []
    cache_res = {}
    if cache_file is not None:
        # incremental update
        cache_res = json.load(open(cache_file, 'r'))
        cache_conf = [name for name in cache_res.keys()]
    
    for conf in tqdm(acl_conf, desc="[+] Crawling ACL", dynamic_ncols=True):
        assert conf.get('name') and conf.get('url') and conf.get('tag')
        url, tag, name = conf['url'], conf['tag'], conf['name']
        if name in cache_conf:
            continue
        res = search_from_acl(url, tag, name, res)

    for conf in tqdm(dblp_conf, desc="[+] Crawling DBLP", dynamic_ncols=True):
        assert conf.get('name') and conf.get('url')
        url, name = conf['url'], conf['name']
        if name in cache_conf:
            continue
        res = search_from_dblp(url, name, res)

    for conf in tqdm(nips_conf, desc="[+] Crawling NeurIPS", dynamic_ncols=True):
        assert conf.get('name') and conf.get('url')
        url, name = conf['url'], conf['name']
        if name in cache_conf:
            continue
        res = search_from_nips(url, name, res)
        
    res.update(cache_res)
    return res

def do_crawl(cache_file=None, force=False):
    if force or cache_file is None or not os.path.exists(cache_file):
        print(f'[+] Crawling papers...')
        res = crawl(None if cache_file is None or not os.path.exists(cache_file) else cache_file)
        with open(cache_file, 'w') as f:
            json.dump(res, f)
    else:
        print(f'[+] Loading from cache...')
        with open(cache_file, 'r') as f:
            res = json.load(f)
    return res

if __name__ == '__main__':
    do_crawl(cache_file='cache/cache.json', force=True)
    