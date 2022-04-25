from constant import init
from searcher import exec_search
from utils import show_res, output_res, special_input



def main():

    indexes, candidates = init()

    while(1):
        mode, threshold, confs, limit = None, None, None, None

        query = input('[+] Enter your query: ')
        if(special_input(query) or query == ''): continue

        print("\n[+] Select search mode:\n\t[1] Exact\n\t[2] Fuzzy")
        select_mode = input('[+] Enter a number between 1 to 2: ')
        if(special_input(select_mode, mode='select_mode')): continue
        if select_mode == '': select_mode = '1'
        mode = 'exact' if select_mode == '1' else 'fuzzy'

        if mode == 'fuzzy':

            threshold = input('\n[+] Enter threshold between 0 and 100 (default: 50): ')
            if(special_input(threshold, mode='threshold')): continue
            if threshold == '': threshold = None
            else: threshold = int(threshold)
            
            limit = input('\n[+] Enter limit >= 0 (default: None): ')
            if(special_input(limit, mode='limit')): continue
            if limit == '': limit = None
            else: limit = int(limit)

        print('\n[+] Enter the list of confs separated by comma\n\tE.g. "ACL,CVPR" or "AAAI" or enter nothing for all confs')
        confs = input('[+] Enter your list of conferences (default: All Confs): ')
        if(special_input(confs)): continue
        if confs == '': confs = None
        else: confs = confs.split(',')


        results = exec_search(indexes, candidates, query, mode, threshold, confs, limit)
        if len(results) == 0: print('[-] No results found.\n'); continue
        show_res(results)
        

        filename = input('\n[+] Enter Save filename: ')
        if(special_input(filename)): continue
        if(filename == ''):
            filename = f'{mode}_{threshold}_{"_".join(confs) if confs else None}_{query}.txt'
        output_res(results, filename)


if __name__ == '__main__':
    main()

