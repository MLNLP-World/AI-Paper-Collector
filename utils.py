import os
import getopt
from constant import open_flag, tip_flag, category_flag

def special_input(input_str, mode=None):
    if input_str == 'q':
        exit('[+] Good bye!')
    elif input_str == '#':
        os.system('clear')
        print(open_flag)
        print(tip_flag)
        return True
    elif input_str == 'h':
        print(category_flag)
        return True
    elif mode == 'select_mode':
        if not input_str in ['1', '2', '']:
            print('[-] Invalid input.\n')
            return True
    elif mode == 'threshold':
        if input_str == '': 
            return False
        if not input_str.isdigit():
            print('[-] Invalid input.\n')
            return True
        input_str = int(input_str)
        if input_str < 0 or input_str > 100:
            print('[-] Invalid input.\n')
            return True
    elif mode == 'limit':
        if input_str == '': 
            return False
        if not input_str.isdigit():
            print('[-] Invalid input.\n')
            return True
        input_str = int(input_str)
        if input_str < 0:
            print('[-] Invalid input.\n')
            return True         
    return False


def parse_args(command):
    try:
        opts, args = getopt.getopt(command.split(), '', ['mode=', 'threshold=', 'conf=', 'limit='])
    except getopt.GetoptError:
        print('[-] Wrong input!')
        return False, None, None, None

    mode = None
    threshold = None
    conf = None
    limit = None
    for opt, arg in opts:
        if opt == '--mode':
            mode = arg
        elif opt == '--threshold':
            threshold = int(arg)
        elif opt == '--conf':
            conf = arg.split(',')
        elif opt == '--limit':
            limit = int(arg)
    if mode is None:
        print('[-] Wrong input!')
        return False, None, None, None
    if mode not in ['fuzzy', 'exact']:
        print('[-] Wrong input!')
        return False, None, None, None
    if threshold is not None:
        if threshold < 0 or threshold > 100:
            print('[-] Wrong input!')
            return False, None, None, None
    if limit is not None:
        if limit < 0:
            print('[-] Wrong input!')
            return False, None, None, None

    return mode, threshold, conf, limit


def check_filename(filename):
    if os.path.dirname(filename) == '':
        filename = os.path.join('output', filename)
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    return filename


def output_res(results, filename):
    try:
        filename = check_filename(filename)
        print('\n[+] Writing results to {}'.format(filename))
        with open(filename, 'w',encoding='utf-8') as f:
            for item in results:
                f.write(f'【{item[0]}】{item[1]}' + '\n\n')
        print('[+] Writing results Done!\n')
        return True
    except:
        print('\n[-] Writing results Failed!\n')
        return False

def show_res(results):
    print('\n[+] Search Results:')
    print('[=] Only show Top-5, Please Save results to see all.\n')
    for i in range(min(5, len(results))):
        print(f'[{i+1}] [{results[i][0]}] {results[i][1]}')
