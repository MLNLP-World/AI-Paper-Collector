import requests
import re
import os
import argparse
from bs4 import BeautifulSoup

# config
parser = argparse.ArgumentParser()
parser.add_argument("--keyword", default='few-shot', type=str)
args = parser.parse_args()

# crawer script
res = {}
# for 2021 ...
urls = [
      'https://aclanthology.org/events/emnlp-2021/',
      'https://aclanthology.org/volumes/2021.findings-emnlp/',
      'https://aclanthology.org/events/acl-2021/',
      'https://aclanthology.org/volumes/2021.findings-acl/',
      'https://aclanthology.org/events/naacl-2021/',
      'https://aclanthology.org/events/emnlp-2020/',
      'https://aclanthology.org/events/emnlp-2020/',
      'https://aclanthology.org/events/acl-2020/',
      'https://aclanthology.org/events/coling-2020/',
]
tags = [
      "^/2021.emnlp*",
      '^/2021.findings*',
      "^/2021.acl*",
      "^/2021.findings*",
      "^/2021.naacl*",
      "^/2020.emnlp*",
      "^/2020.findings*",
      "^/2020.acl*",
      "^/2020.coling*",
]
names = [
      'EMNLP2021',
      'EMNLP2021 findings',
      'ACL2021',
      'ACL2021 findings',
      'NAACL2021',
      'EMNLP2020',
      'EMNLP2020 findings',
      'ACL2020',
      'COLING2020',
]
for url, tag, name in zip(urls, tags, names):
  print(f'name:{name}\turl:{url}')
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'html.parser')

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

# for 2019...
urls = [
      'https://aclanthology.org/events/acl-2019/',
      'https://aclanthology.org/events/emnlp-2019/',
      'https://aclanthology.org/events/naacl-2019/',
]
tags = [
      "^/P19-*",
      "^/D19-*",
      "^/N19-*",
]
names = [
      'ACL2019',
      'EMNLP2019',
      'NAACL2019',
]
for url, tag, name in zip(urls, tags, names):
  print(f'name:{name}\turl:{url}')
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'html.parser')

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

# for others
urls = [
    'https://dblp.org/db/conf/nips/neurips2020.html',
    'https://dblp.org/db/conf/nips/nips2019.html',
    'https://dblp.org/db/conf/iclr/iclr2021.html',
    'https://dblp.org/db/conf/iclr/iclr2020.html',
    'https://dblp.org/db/conf/iclr/iclr2019.html',
    'https://dblp.org/db/conf/icml/icml2021.html',
    'https://dblp.org/db/conf/icml/icml2020.html',
    'https://dblp.org/db/conf/icml/icml2019.html',
    'https://dblp.org/db/conf/aaai/aaai2021.html',
    'https://dblp.org/db/conf/aaai/aaai2020.html',
    'https://dblp.org/db/conf/aaai/aaai2019.html',
    'https://dblp.org/db/conf/ijcai/ijcai2021.html',
    'https://dblp.org/db/conf/ijcai/ijcai2020.html',
    'https://dblp.org/db/conf/ijcai/ijcai2019.html',
    'https://dblp.org/db/conf/cvpr/cvpr2021.html',
    'https://dblp.org/db/conf/cvpr/cvpr2020.html',
    'https://dblp.org/db/conf/cvpr/cvpr2019.html',
    'https://dblp.org/db/conf/iccv/iccv2019.html',
    'https://dblp.org/db/conf/mm/mm2021.html',
    'https://dblp.org/db/conf/mm/mm2020.html',
    'https://dblp.org/db/conf/mm/mm2019.html',
    'https://dblp.org/db/conf/kdd/kdd2021.html',
    'https://dblp.org/db/conf/kdd/kdd2020.html',
    'https://dblp.org/db/conf/kdd/kdd2019.html',
    'https://dblp.org/db/conf/cikm/cikm2021.html',
    'https://dblp.org/db/conf/cikm/cikm2020.html',
    'https://dblp.org/db/conf/cikm/cikm2019.html',
    'https://dblp.org/db/conf/sigir/sigir2021.html',
    'https://dblp.org/db/conf/sigir/sigir2020.html',
    'https://dblp.org/db/conf/sigir/sigir2019.html',


]
names = [
    'NIPS2020',
    'NIPS2019',
    'ICLR2021',
    'ICLR2020',
    'ICLR2019',
    'ICML2021',
    'ICML2020',
    'ICML2019',
    'AAAI2021',
    'AAAI2020',
    'AAAI2019',
    'IJCAI2021',
    'IJCAI2020',
    'IJCAI2019',
    'CVPR2021',
    'CVPR2020',
    'CVPR2019',
    'ICCV2019',
    'MM2021',
    'MM2020',
    'MM2019',
    'KDD2021',
    'KDD2020',
    'KDD2019',
    'CIKM2021',
    'CIKM2020',
    'CIKM2019',
    'SIGIR2021',
    'SIGIR2020',
    'SIGIR2019',
]
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
for url, name in zip(urls, names):
  print(f'name:{name}\turl:{url}')
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'html.parser')

  res[name] = []
  for paper_item in soup.find_all(class_='title', itemprop="name"):
      items = [item.string if item.string else item for item in paper_item.contents]
      try:
        paper = "".join([item for item in items if isinstance(item, str)])
      except:
        import pdb
        pdb.set_trace()
      res[name].append(paper)

keyword = args.keyword
with open('all_papers.txt', 'w') as f1:
  with open(f'{keyword}_papers.txt', 'w') as f2:
    for conf, papers in res.items():
      for paper in papers:
        f1.write(f'【{conf}】{paper}' + '\n\n')
        if keyword in paper.lower():
          f2.write(f'【{conf}】{paper}' + '\n\n')
