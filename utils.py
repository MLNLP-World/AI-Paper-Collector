import os
import json
import getopt


def parse_args(command):
    try:
        opts, args = getopt.getopt(command.split(), '', ['mode=', 'threshold=', 'conf='])
    except getopt.GetoptError:
        print('[-] Wrong input!')
        return False, None, None

    mode = None
    threshold = None
    conf = None
    for opt, arg in opts:
        if opt == '--mode':
            mode = arg
        elif opt == '--threshold':
            threshold = int(arg)
        elif opt == '--conf':
            conf = arg.split(',')
    if mode is None:
        print('[-] Wrong input!')
        return False, None, None
    if mode not in ['fuzzy', 'exact']:
        print('[-] Wrong input!')
        return False, None, None
    if threshold is not None:
        if threshold < 0 or threshold > 100:
            print('[-] Wrong input!')
            return False, None, None

    return mode, threshold, conf

def check_filename(filename):
    if os.path.dirname(filename) == '':
        filename = os.path.join('output', filename)
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    return filename


def output_res(results, filename):
    try:
        filename = check_filename(filename)
        print('[+] Writing results to {}'.format(os.path.join('output', filename)))
        with open(filename, 'w') as f:
            for item in results:
                f.write(f'【{item[0]}】{item[1]}' + '\n\n')
        print('[+] Writing results Done!')
        return True
    except:
        print('[-] Writing results Failed!')
        return False