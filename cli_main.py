import argparse
from constant import init
from searcher import exec_search
from utils import show_res, output_res


def set_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--query', '-q', type=str, help='Query to search for.', required=True)
    parser.add_argument('--mode', '-m', type=str, default='exact', choices=['fuzzy', 'exact'], help='search mode')
    parser.add_argument('--threshold', '-t', type=int, default=50, help='fuzzy search threshold')
    parser.add_argument('--limit', '-l', type=int, default=None, help='fuzzy search limit')
    parser.add_argument('--conf', '-c', type=str, default=None, help='conferences to search')
    parser.add_argument("--output", "-o", type=str, default=None, help="output file")

    parser.add_argument('--force', '-f', action='store_true', help='force to update the cache file incrementally')

    args = parser.parse_args()

    if args.conf:
        args.conf = args.conf.split(',')

    if not args.output:
        args.output = f'{args.mode}_{args.threshold}_{"_".join(args.conf) if args.conf else None}_{args.query}.txt'

    return args

def main():
    args = set_args()

    indexes, candidates = init(args.force)

    results = exec_search(
        indexes, 
        candidates, 
        args.query, 
        args.mode, 
        args.threshold, 
        args.conf, 
        args.limit
    )

    if len(results) == 0: 
        print('[-] No results found.')
    else:
        show_res(results)
        output_res(results, args.output)

if __name__ == '__main__':
    main()



