import math
import numpy as np
from distance import *


def confusion_matrix(aligned_matching, true_matching):
    aligned_set = set()
    true_set = set(true_matching)
    for t in aligned_matching:
        v = t[0]
        u = t[1]
        if v >= 0 and u >= 0:
            aligned_set.add((v, u))
    TP = len(aligned_set & true_set)
    FP = len(aligned_set - true_set)
    FN = len(true_set - aligned_set)
    return TP, FP, FN


def accuracy(aligned_matching, true_matching):
    tp, _, _ = confusion_matrix(aligned_matching, true_matching)
    acc = tp / len(true_matching)
    return acc


def mean_average_precision(true_matching, ctx0, ctx1, dis='dcmn'):
    rank_rev = 0
    if dis == 'dcmn':
        for v, u in true_matching:
            mat_dis = dynamic_commonality(ctx0[v], ctx1[u])
            r = 1
            for w in ctx1.keys():
                dis = dynamic_commonality(ctx0[v], ctx1[w])
                if dis < mat_dis:
                    r += 1
            rank_rev += 1/r
    if dis == 'scmn':
        for v, u in true_matching:
            mat_dis = static_commonality(ctx0[v], ctx1[u])
            r = 1
            for w in ctx1.keys():
                dis = static_commonality(ctx0[v], ctx1[w])
                if dis < mat_dis:
                    r += 1
            rank_rev += 1/r
    return rank_rev / len(true_matching)


def edge_correctness(aligned_matching, graph0, graph1):
    graph0_aligned = dict()
    for t in aligned_matching:
        v = t[0]
        u = t[1]
        if v >= 0 and u >= 0:
            graph0_aligned[v] = u

    num_edge = 0
    for v, u in graph0.edges:
        if v in graph0_aligned.keys() and u in graph0_aligned.keys():
            x = graph0_aligned[v]
            y = graph0_aligned[u]
            if graph1.has_edge(x, y):
                num_edge += 1

    return num_edge/len(graph0.edges)


def induced_conserved_structure(aligned_matching, graph0, graph1):
    graph1_aligned = dict()
    num_edge = 0
    num_all_edge = 0
    induced_node = set()
    for t in aligned_matching:
        v = t[0]
        u = t[1]
        if v >= 0 and u >= 0:
            graph1_aligned[u] = v
            induced_node.add(u)

    for v, u in graph1.edges:
        if v in graph1_aligned.keys() and u in graph1_aligned.keys():
            x = graph1_aligned[v]
            y = graph1_aligned[u]
            if graph0.has_edge(x, y):
                num_edge += 1

    for v, u in graph1.edges:
        if v in induced_node and u in induced_node:
            num_all_edge += 1
    return num_edge/num_all_edge

