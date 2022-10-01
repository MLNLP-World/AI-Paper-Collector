import json
import os
import re
import yaml
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
}

def search_from_iclr(url, name, res):
    r = requests.get(url, headers=HEADERS)
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

def search_abs_from_nips(url):
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")
    abstract = soup.find(
        lambda tag: tag.name == "h4" and 'Abstract' in tag.text
    ).next_sibling.next_sibling.text.strip()
    return abstract

def search_from_nips(url, name, res):
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")
    if name not in res:
        res[name] = []
    url_prefix = "https://" + url[8:].split("/")[0]
    for paper_item in soup.find(class_="col").ul.find_all("li"):
        paper_url = url_prefix + paper_item.a["href"]
        if paper_item.i.string is not None:
            paper_author = [author.strip() for author in paper_item.i.string.split(',')]
        else:
            paper_author = []
        try:
            paper_abstract = search_abs_from_nips(paper_url)
        except:
            print(f"Skip url:{paper_url}")
            paper_abstract = ""

        res[name].append(
            {
                "paper_name": paper_item.a.string, 
                "paper_url": paper_url,
                "paper_authors": paper_author,
                "paper_abstract": paper_abstract,
            }
        )
    return res


def search_from_acl(url, tag, name, res):
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")
    if name not in res:
        res[name] = []
    for tp in soup.find_all("p", class_="d-sm-flex align-items-stretch"):
        cls = tp.find("strong")
        for paper_item in cls.find_all(href=re.compile(tag), class_="align-middle"):
            items = [item.string if item.string else item for item in paper_item.contents]

            paper = "".join([item for item in items if isinstance(item, str)])
            paper_url = "https://aclanthology.org" + paper_item["href"]
            if tp.next_sibling is not None and tp.next_sibling.has_attr("id") and "abstract" in tp.next_sibling["id"]:
                paper_abstract = tp.next_sibling.text
            else:
                print(f"Skip url:{paper_url}")
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


def search_abs_from_dblp(url):
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")

    if 'ieee' in r.url:
        abstract = yaml.safe_load(soup.find(
            lambda tag: tag.name == 'script' and 'xplGlobal.document.metadata' in tag.text
        ).text.split('\n\t')[-1].strip()[28:-1])['abstract']

    elif 'acm' in r.url:
        abstract = soup.find(class_="abstractSection").p.string.strip()

    elif 'openreview' in r.url:
        url = 'https://api.openreview.net/notes?forum=' + r.url.split("=")[-1]
        r = requests.get(url, headers=headers)
        abstract = r.json()["notes"][-1]["content"]["abstract"]

    elif 'mlr' in r.url:
        abstract = soup.find(id="abstract").string.strip()

    elif 'aaai' in r.url:
        abstract = soup.find(class_="abstract").p.string.strip()

    elif 'ijcai' in r.url:
        abstract = soup.find(class_="proceedings-detail").find(class_="col-md-12").string.strip()

    elif 'springer' in r.url:
        abstract = soup.find(id="Abs1-content").next_element.text.strip()

    elif 'jmlr' in r.url:
        abstract = soup.find(class_="abstract").string.strip()

    else:
        abstract = ""

    return abstract


def search_from_dblp(url, name, res):
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")
    if name not in res:
        res[name] = []

    for paper_item in soup.find_all("li", class_="entry"):
        paper_url = paper_item.find("li", class_="drop-down").div.a["href"]
        paper_name = paper_item.find(class_="title", itemprop="name")

        paper_authors = [
            re.sub("\d", "", author["title"]).strip()
            for author in paper_item.find_all(class_=None, itemprop="name") if author.has_attr("title")]

        items = [item.string if item.string else item for item in paper_name.contents]
        paper = "".join([item for item in items if isinstance(item, str)])
        try:
            paper_abstract = search_abs_from_dblp(paper_url)
        except:
            print(f"Skip url:{paper_url}")
            paper_abstract = ""
        res[name].append(
            {
                "paper_name": paper, 
                "paper_url": paper_url,
                "paper_authors": paper_authors,
                "paper_abstract": paper_abstract,
            }
        )
    return res


def search_abs_from_thecvf(url):
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")
    abstract = soup.find(id="abstract").text.strip()
    return abstract

def search_from_thecvf(url, name, res):
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")
    if name not in res:
        res[name] = []
        
    for paper_item in soup.find_all("dt", class_="ptitle"):
        paper_url = "https://openaccess.thecvf.com" + paper_item.a["href"]
        paper = paper_item.a.string
        paper_authors = [author.string for author in paper_item.next_sibling.next_sibling.find_all('a', href='#')]
        try:
            paper_abstract = search_abs_from_thecvf(paper_url)
        except:
            print(f"Skip url:{paper_url}")
            paper_abstract = ""
        res[name].append(
            {
                "paper_name": paper, 
                "paper_url": paper_url,
                "paper_authors": paper_authors,
                "paper_abstract": paper_abstract,
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
        
    for conf in tqdm(dblp_conf, desc="[+] Crawling DBLP", dynamic_ncols=True):
        assert conf.get("name") and conf.get("url")
        url, name = conf["url"], conf["name"]
        if name in cache_conf:
            continue
        res = search_from_dblp(url, name, res)

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
