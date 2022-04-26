import os
import json
import ast
import argparse
from crawler import do_crawl

def set_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--issue', '-i', type=str, help='input issue', required=True)
    args = parser.parse_args()
    return args

def parse_issue(issue):
    try:
        info = ast.literal_eval(issue)
        assert isinstance(info, list)
        assert len(info) > 0 and info[0].get('url') and info[0].get('name') and info[0].get('source')
    except:
        raise Exception('[-] Wrong input!')
    return info

def add_list(args):
    print('[+] Add list...')
    info = parse_issue(args.issue)
    re_info = {}
    for item in info:
        assert item.get('source') in ['nips', 'acl', 'dblp']
        source = item.get('source')
        if source not in re_info:
            re_info[source] = []
        del item['source']
        re_info[source].append(item)

    for source in re_info.keys():
        path = os.path.join('conf', source + '_conf.json')
        confs = json.load(open(path, 'r')) # [{'url': '', 'name': ''}]
        for item in re_info[source]:
            # need to mannally check duplicated conferences
            confs.append(item)
        json.dump(confs, open(path, 'w'), indent=4)
    print('[+] Add list Done!')

def main():
    args = set_args()
    add_list(args)
    do_crawl(cache_file='cache/cache.json', force=True)
    
if __name__ == '__main__':
    main()

