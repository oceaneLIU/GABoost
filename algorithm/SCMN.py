import networkx as nx
import numpy as np
import time
import threading
import multiprocessing as mp
from functools import partial
from metrics import *
from distance import *
from scipy.optimize import linear_sum_assignment

class SCMN:

    def __init__(self, graph1: nx.DiGraph, graph2: nx.DiGraph):
        self.graph1 = graph1
        self.graph2 = graph2
        self.node_type = set()
        self.edge_type = set()
        self.node_group_by_type_graph1 = dict()
        self.node_group_by_type_graph2 = dict()
        self.type_encoder = dict()
        self.type_decoder = dict()
        self.cost_matrix = dict()
        for v in self.graph1.nodes:
            node_type = self.graph1.nodes[v]['type']
            if node_type in self.node_group_by_type_graph1.keys():
                self.node_group_by_type_graph1[node_type].add(v)
            else:
                self.node_group_by_type_graph1[node_type] = {v}
            for u in self.graph1.neighbors(v):
                self.edge_type.add(self.graph1[v][u]['type'])

        for v in self.graph2.nodes:
            node_type = self.graph2.nodes[v]['type']
            if node_type in self.node_group_by_type_graph2.keys():
                self.node_group_by_type_graph2[node_type].add(v)
            else:
                self.node_group_by_type_graph2[node_type] = {v}
            for u in self.graph2.neighbors(v):
                self.edge_type.add(self.graph2[v][u]['type'])

        for t in self.node_group_by_type_graph1.keys():
            self.node_type.add(t)
        for t in self.node_group_by_type_graph2.keys():
            self.node_type.add(t)
        for t in self.node_type:
            if t not in self.node_group_by_type_graph1.keys():
                self.node_group_by_type_graph1[t] = set()
            if t not in self.node_group_by_type_graph2.keys():
                self.node_group_by_type_graph2[t] = set()
        # Encode node and edge type
        ind = 0
        for i in self.node_type:
            for j in self.edge_type:
                self.type_encoder[(i, j)] = ind
                self.type_decoder[ind] = (i, j)
                ind += 1

    def basic_static_node_context(self, graph: nx.DiGraph):
        static_node_context = dict()
        type_len = len(self.type_decoder.keys())
        ctx_len = 2 * type_len
        for v in graph.nodes:
            ctx = np.zeros(ctx_len)
            for u in graph.neighbors(v):
                et = graph[v][u]['type']
                nt = graph.nodes[u]['type']
                ind = self.type_encoder[(nt, et)]
                ctx[ind] += 1
            for w in graph.predecessors(v):
                et = graph[w][v]['type']
                nt = graph.nodes[w]['type']
                ind = self.type_encoder[(nt, et)] + type_len
                ctx[ind] += 1
            static_node_context[v] = ctx
        return static_node_context

    def get_static_matching(self, t, node_context1, node_context2):

        matching = []
        type_len = len(self.type_decoder.keys())
        ctx_len = 2 * type_len

        node1_encoded = []
        node2_encoded = []
        node_bipartite_decoder_graph1 = dict()
        node_bipartite_decoder_graph2 = dict()
        ind = 0
        for v in self.node_group_by_type_graph1[t]:
            node_bipartite_decoder_graph1[ind] = v
            node1_encoded.append(ind)
            ind += 1
        ind = 0
        for v in self.node_group_by_type_graph2[t]:
            node_bipartite_decoder_graph2[ind] = v
            node2_encoded.append(ind)
            ind += 1

        n_thread = len(self.node_type)
        n_per_thread = len(node1_encoded)//n_thread
        node1_encoded_sliced = []
        for i in range(0, n_per_thread-1):
            node1_encoded_sliced.append(node1_encoded[i*n_per_thread:(i+1)*n_per_thread])
        node1_encoded_sliced.append(node1_encoded[(n_per_thread-1)*n_per_thread:])

        self.cost_matrix[t] = np.zeros((len(node1_encoded), len(node2_encoded)))
        thread_list = [threading.Thread(target=self.get_distance_mp_static, args=(t, n, node2_encoded,
                                                               node_bipartite_decoder_graph1, node_bipartite_decoder_graph2,
                                                               node_context1, node_context2, )) for n in node1_encoded_sliced]
        for thread in thread_list:
            thread.start()
        for thread in thread_list:
            thread.join()
        row_ind, col_ind = linear_sum_assignment(self.cost_matrix[t])
        for i in range(0, len(row_ind)):
            v = row_ind[i]
            u = col_ind[i]
            matching.append((node_bipartite_decoder_graph1[v], node_bipartite_decoder_graph2[u]))
        return matching

    def get_distance_mp_static(self, t, node1_encoded, node2_encoded, node_bipartite_decoder_graph1,
                               node_bipartite_decoder_graph2, node_context1, node_context2):
        for i in node1_encoded:
            original_node1 = node_bipartite_decoder_graph1[i]
            ctx1 = node_context1[original_node1]
            for j in node2_encoded:
                original_node2 = node_bipartite_decoder_graph2[j]
                ctx2 = node_context2[original_node2]
                dis = static_commonality(ctx1, ctx2)
                self.cost_matrix[t][i][j] = dis

    def get_matching(self, cpu_num):

        #with mp.Pool(cpu_num) as pool:
        #    results = pool.map(self.basic_static_node_context, [self.graph1, self.graph2])
        static_ctx1 = self.basic_static_node_context(self.graph1)
        static_ctx2 = self.basic_static_node_context(self.graph2)

        with mp.Pool(cpu_num) as pool:
            results = pool.map(partial(self.get_static_matching, node_context1=static_ctx1, node_context2=static_ctx2),
                               self.node_type)
        matching = []
        for r in results:
            matching += r
        return matching
