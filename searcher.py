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

def fuzzy_search(indexes, candidates, query, threshold=None, confs=None):
    if threshold is None:
        threshold = 50
    sl = process.extractWithoutOrder(query, candidates, score_cutoff=threshold)
    results = sorted(sl, key=lambda i: i[1], reverse=True)
    results = [item[2] for item in results if item[1] >= threshold]
    results = [indexes[idx] for idx in results]
    if confs is not None:
        results = [item for item in results if check_conf(item[0], confs)]
    return results


def exact_search(indexes, query, confs=None):
    results = []
    query = query.lower()
    results = [item for item in indexes if query in item[1].lower()]
    if confs is not None:
        results = [item for item in results if check_conf(item[0], confs)]
    return results

