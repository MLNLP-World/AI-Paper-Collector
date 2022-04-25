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

def exec_search(indexes, candidates, query, mode, threshold, confs, limit):
    if mode == 'fuzzy':
        results = fuzzy_search(indexes, candidates, query, threshold, confs, limit)
    elif mode == 'exact':
        results = exact_search(indexes, query, confs)
    return results

