import functools
import re

from thefuzz import process


def build_index(res):
    idx = 0
    indexes = []
    candidates = {}
    for conf, papers in res.items():
        for paper in papers:
            indexes.append([conf, paper, idx])
            candidates[idx] = paper
            idx += 1
    return indexes, candidates


def check_conf(conf, input_confs):
    return any(input_conf.lower() in conf.lower() for input_conf in input_confs)


def fuzzy_search(indexes, candidates, query, threshold=None, confs=None, limit=None):
    if threshold is None:
        threshold = 50

    # Note that threshold cannot be too large, otherwise the search results will be too few
    # sl: [(paper, score, index),...]
    sl = process.extractWithoutOrder(query, candidates, score_cutoff=threshold)

    # sort by score
    results = sorted(sl, key=lambda i: i[1], reverse=True)

    # convert to papers: [(conf, paper, index),...]
    results = [indexes[item[2]] for item in results]

    # filter by confs
    if confs is not None:
        results = [item for item in results if check_conf(item[0], confs)]

    # filter by limit
    if limit is not None:
        results = results[:limit]

    return results


def exact_search(indexes, query, confs=None):
    results = []
    query = query.lower()
    results = [item for item in indexes if query in item[1].lower()]
    if confs is not None:
        results = [item for item in results if check_conf(item[0], confs)]
    return results


def sort_results(results):
    def cmp_by_year(x, y):
        x_year = re.search(r"\d{4}", x[0]).group()
        y_year = re.search(r"\d{4}", y[0]).group()
        if x_year < y_year:
            return 1
        elif x_year > y_year:
            return -1
        else:
            return 0

    return sorted(results, key=functools.cmp_to_key(cmp_by_year))


def exec_search(indexes, candidates, query, mode, threshold, confs, limit):
    if mode == "fuzzy":
        results = fuzzy_search(indexes, candidates, query, threshold, confs, limit)
    elif mode == "exact":
        results = exact_search(indexes, query, confs)
    results = sort_results(results)
    return results
