from constant import init
from searcher import exec_search, boolean_search
from utils import show_res, output_res, special_input



def main():

    indexes, candidates, postings, posting_indexes = init()
    modes_map = {"1": "exact", "2": "fuzzy", "3": "boolean"}

    while(1):
        mode, threshold, confs, limit = None, None, None, None

        query = input('[+] Enter your query: ')
        if(special_input(query) or query == ''): continue

        print("\n[+] Select search mode:\n\t[1] Exact\n\t[2] Fuzzy\n\t[3] Boolean")
        select_mode = input('[+] Enter a number between 1 to 3: ')
        if(special_input(select_mode, mode='select_mode')): continue
        if select_mode == '': select_mode = '1'
        mode = modes_map[select_mode]

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

        if mode in ['fuzzy', 'exact']:
            results = exec_search(indexes, candidates, query, mode, threshold, confs, limit)
        elif mode == 'boolean':
            results = boolean_search(query, postings, posting_indexes, confs)
        else:
            pass # TODO
        if len(results) == 0: print('[-] No results found.\n'); continue
        show_res(results)
        

        filename = input(f'\n[+] Enter Saving filename (default: [mode]_[threshold]_[confs]_[query].txt): ')
        if(special_input(filename)): continue
        if(filename == ''):
            filename = f'{mode}_{threshold}_{"_".join(confs) if confs else None}_{query}.txt'
        output_res(results, filename)


if __name__ == '__main__':
    main()

