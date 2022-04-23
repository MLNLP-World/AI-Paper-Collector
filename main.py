import os
import warnings
from crawler import do_crawl
from utils import parse_args, output_res
from searcher import build_index, fuzzy_search, exact_search
warnings.filterwarnings("ignore")

open_flag = """
  ___  _____ _____                     _               
 / _ \|_   _/  ___|                   | |              
/ /_\ \ | | \ `--.  ___  __ _ _ __ ___| |__   ___ _ __ 
|  _  | | |  `--. \/ _ \/ _` | '__/ __| '_ \ / _ \ '__|
| | | |_| |_/\__/ /  __/ (_| | | | (__| | | |  __/ |   
\_| |_/\___/\____/ \___|\__,_|_|  \___|_| |_|\___|_|  

AI-Search-Engine V0.1

Tips:
- enter "q" into any input to exit the program.
- enter "#" into any input to clear the screen.
- enter "help" into any input to see the help.
- enter nothing means search with default mode: exact.
"""

help_flag = """

Search Categories: 
- [ACL 2019-2021] [EMNLP 2019-2021] [NAACL 2019-2021] [COLING 2020]
- [CVPR 2019-2021] [ECCV 2020] [ICCV2019] [ACMMM 2019-2021]
- [ICLR 2019-2021] [ICML 2019-2021] [AAAI 2019-2021] [IJCAI 2019-2021]
- [SIGIR 2019-2021] [KDD 2019-2021] [CIKM 2019-2021] [WSDM 2019-2022]
- [WWW 2019-2021] [ECIR 2019-2022]

Search Commands:
- --mode <mode: fuzzy|exact> [optional: --threshold <num>] [optional: --conf <string/list(string)>]
- e.g. "--mode fuzzy --threshold 50" means fuzzy search with similarity >= 50 with all papers
- e.g. "--mode exact --conf ACL" means exact search with all papers in ACL
- e.g. "--mode exact --conf ACL,CVPR" means exact search with all papers in ACL and CVPR
- Note that the threshold is only for fuzzy search from 0 to 100 (default: 50)
- Note that the list of confs should be separated by comma (e.g. "ACL,CVPR")

"""


indexes, candidates = None, None

def special_input(input_str):
    if input_str == 'q':
        exit('[+] Good bye!')
    elif input_str == '#':
        os.system('clear')
        print(open_flag)
        return True
    elif input_str == 'help':
        print(help_flag)
        return True
    return False

def exec_search(query, mode, threshold, confs):
    if mode == 'fuzzy':
        results = fuzzy_search(indexes, candidates, query, threshold, confs)
    elif mode == 'exact':
        results = exact_search(indexes, query, confs)
    return results

def init():
    global indexes, candidates
    print(open_flag)
    print("[+] Initializing System...")
    cache_file = 'cache/cache.json'
    res = do_crawl(cache_file)
    indexes, candidates = build_index(res)
    print("[+] Enter 'help' into any input for more information when first starting.")

def main():

    while(1):
        query = input('[+] Enter your query: ')
        if(special_input(query) or query == ''): continue

        command = input('[+] Enter Search Commands: ')
        if(special_input(command)): continue
        if(command == ''): command = '--mode exact'
        mode, threshold, confs = parse_args(command)
        if(mode == False): continue
        results = exec_search(query, mode, threshold, confs)

        print('[+] Search Results:')
        print('[=] Only show Top-5, Please Save results to see all.')
        for i in range(min(5, len(results))):
            print(f'[{i+1}] [{results[i][0]}] {results[i][1]}')
        
        command = input('[+] Enter Save filename: ')
        if(special_input(command)): continue
        if(command == ''): command = f'{query}_{mode}_{threshold}_{confs}.txt'
        output_res(results, command)

if __name__ == '__main__':
    init()
    main()


        
 












