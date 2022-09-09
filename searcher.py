import functools
import re
from thefuzz import process
from collections import defaultdict


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


def get_posting_list(res):
    idx = 0
    posting_indexes = []
    postings = defaultdict(dict)
    for conf, papers in res.items():
        for paper in papers:
            posting_indexes.append([conf, paper, idx])
            for token in paper['paper_name'].strip().split():
                token = token.lower()
                postings[token][idx] = 1
            idx += 1
    return postings, posting_indexes


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


def boolean_search(query, postings, posting_indexes, confs=None):
    def _op(operator, left_operand: set, right_operand=None):
        assert operator in ["AND", "OR", "NOT"], "Operator should be in ['AND', 'OR', 'NOT'], but get {}!!!".format(operator)
        if operator == "AND":
            assert right_operand is not None, "The right operand should not be None when the operator is AND!!!"
            return left_operand.intersection(right_operand)
        elif operator == 'OR':
            assert right_operand is not None, "The right operand should not be None when the operator is OR!!!"
            return left_operand.union(right_operand)
        else:
            return all_docs - left_operand

    def _parse_query(query_units: list):
        operator_stack = []
        operand_stack = []

        for unit in query_units:
            if unit in ["AND", "OR", "NOT", "(", ")"]: # operators
                cur_prece = precedence[unit]
                stack_prece = -100 if len(operator_stack) == 0 else precedence[unit]
                if cur_prece > stack_prece:
                    operator_stack.append(unit)
                else: # can calculate the operators in the stack with lower of eq precedence
                    if unit == ")":
                        while len(operator_stack) and operator_stack[-1] != "(":
                            op = operator_stack.pop()
                            left_operand = operand_stack.pop()
                            right_operand = operand_stack.pop() if op != "NOT" else None
                            res = _op(op, left_operand, right_operand)
                            operand_stack.append(res)
                        operator_stack.pop() # popout "("
                    else:
                        while len(operator_stack) and operator_stack[-1] != "(" and cur_prece <= precedence[operator_stack[-1]]:
                            op = operator_stack.pop()
                            left_operand = operand_stack.pop()
                            right_operand = operand_stack.pop() if op != "NOT" else None
                            res = _op(op, left_operand, right_operand)
                            operand_stack.append(res)
                        operator_stack.append(unit)
            else: # operands
                try:
                    operand_stack.append(set(postings[unit].keys()))
                except KeyError:
                    operand_stack.append(set())
        
        while len(operator_stack):
            op = operator_stack.pop()
            left_operand = operand_stack.pop()
            right_operand = operand_stack.pop() if op != "NOT" else None
            res = _op(op, left_operand, right_operand)
            operand_stack.append(res)
        
        assert len(operand_stack) == 1, "Operand_stack should contain only one element after processing, but length is {}".format(len(operand_stack))
        return operand_stack[-1]

    # define precedences
    precedence = {}
    precedence['NOT'] = 3
    precedence['AND'] = 2
    precedence['OR'] = 1
    precedence['('] = 100
    precedence[')'] = -100

    all_docs = set([str(x) for x in range(len(posting_indexes))])
    query = "( ".join(" )".join(query.split(")")).split("(")) # add space after "(" and before ")"
    query_units = query.split()

    cand_ids = _parse_query(query_units)
    results = [posting_indexes[x] for x in cand_ids]
    if confs is not None:
        results = [item for item in results if check_conf(item[0], confs)]
    return results


def sort_results(results):
    def cmp_by_year(x, y):
        x_year = re.search(r'\d{4}', x[0]).group()
        y_year = re.search(r'\d{4}', y[0]).group()
        if x_year < y_year: return 1
        elif x_year > y_year: return -1
        else: return 0
    return sorted(results, key=functools.cmp_to_key(cmp_by_year))


def exec_search(indexes, candidates, query, mode, threshold, confs, limit):
    if mode == 'fuzzy':
        results = fuzzy_search(indexes, candidates, query, threshold, confs, limit)
    elif mode == 'exact':
        results = exact_search(indexes, query, confs)
    results = sort_results(results)
    return results
