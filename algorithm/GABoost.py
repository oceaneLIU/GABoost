import networkx as nx
import numpy as np
import time
import threading
import multiprocessing as mp
from functools import partial
from metrics import *
from distance import *
from scipy.optimize import linear_sum_assignment


class GABoost:

    def __init__(self, graph1: nx.DiGraph, graph2: nx.DiGraph, initial_alignment: list):
        self.graph1 = graph1
        self.graph2 = graph2
        self.initial_alignment = initial_alignment
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

    def dynamic_vertex_context(self, graph, index, matching):
        ctx = dict()
        for v in graph.nodes:
            ctx[v] = set()

        for v in graph.nodes:
            for u in graph.neighbors(v):
                et = graph[v][u]['type']
                for i in range(0, len(matching)):
                    if index == 'left':
                        if matching[i][0] == u:
                            dc = i*1000+et*10+0
                            ctx[v].add(dc)
                            break
                    if index == 'right':
                        if matching[i][1] == u:
                            dc = i*1000+et*10+0
                            ctx[v].add(dc)
                            break
            for w in graph.predecessors(v):
                et = graph[w][v]['type']
                for i in range(0, len(matching)):
                    if index == 'left':
                        if matching[i][0] == w:
                            dc = i*1000+et*10+1
                            ctx[v].add(dc)
                            break
                    if index == 'right':
                        if matching[i][1] == w:
                            dc = i*1000+et*10+1
                            ctx[v].add(dc)
                            break
        return ctx

    def get_dynamic_matching(self, t, node_context1, node_context2):
        matching = []
        sum_cost = 0

        # 1. Encode node
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

        # 2. Get pairwise node distance
        n_thread = len(self.node_type)
        n_per_thread = len(node1_encoded) // n_thread
        node1_encoded_sliced = []
        for i in range(0, n_per_thread - 1):
            node1_encoded_sliced.append(node1_encoded[i * n_per_thread:(i + 1) * n_per_thread])
        node1_encoded_sliced.append(node1_encoded[(n_per_thread - 1) * n_per_thread:])

        self.cost_matrix[t] = np.zeros((len(node1_encoded), len(node2_encoded)))
        thread_list = [threading.Thread(target=self.get_distance_mp_dynamic, args=(t, n, node2_encoded,
                                                                           node_bipartite_decoder_graph1,
                                                                           node_bipartite_decoder_graph2,
                                                                           node_context1, node_context2)) for n in node1_encoded_sliced]
        for thread in thread_list:
            thread.start()
        for thread in thread_list:
            thread.join()
        row_ind, col_ind = linear_sum_assignment(self.cost_matrix[t])

        for i in range(0, len(row_ind)):
            v = row_ind[i]
            u = col_ind[i]
            matching.append((node_bipartite_decoder_graph1[v], node_bipartite_decoder_graph2[u]))
            sum_cost += self.cost_matrix[t][v][u]
        return matching, sum_cost

    def get_distance_mp_dynamic(self, t, node1_encoded, node2_encoded, node_bipartite_decoder_graph1,
                                node_bipartite_decoder_graph2, node_context1, node_context2):

        for i in node1_encoded:
            original_node1 = node_bipartite_decoder_graph1[i]
            for j in node2_encoded:
                original_node2 = node_bipartite_decoder_graph2[j]
                if original_node1 >= 0 and original_node2 >= 0:
                    dis = dynamic_commonality(node_context1[original_node1], node_context2[original_node2])
                    self.cost_matrix[t][i][j] = dis

    def get_matching(self, cpu_num):

        iteration = 1
        matching = self.initial_alignment
        start = time.time()
        with mp.Pool(cpu_num) as pool:
            results_ctx = pool.starmap(partial(self.dynamic_vertex_context, matching=matching),
                                       [(self.graph1, 'left'), (self.graph2, 'right')])
            ctx1 = results_ctx[0]
            ctx2 = results_ctx[1]
        with mp.Pool(cpu_num) as pool:
            results = pool.map(partial(self.get_dynamic_matching, node_context1=ctx1, node_context2=ctx2),
                               self.node_type)
        matching = []
        sum_cost = 0
        for r, c in results:
            matching += r
            sum_cost += c
        prev_cost = sum_cost
        end = time.time()
        print('Iteration\t%d\truntime\t%.4f\tdcmn\t%d' % (iteration, end - start, -sum_cost))

        while iteration == 1 or prev_cost != sum_cost:
            start = time.time()
            with mp.Pool(2) as pool:
                results_ctx = pool.starmap(partial(self.dynamic_vertex_context, matching=matching),
                                           [(self.graph1, 'left'), (self.graph2, 'right')])
                ctx1 = results_ctx[0]
                ctx2 = results_ctx[1]

            with mp.Pool(cpu_num) as pool:
                results = pool.map(partial(self.get_dynamic_matching, node_context1=ctx1, node_context2=ctx2),
                                   self.node_type)
            matching = []
            prev_cost = sum_cost
            sum_cost = 0
            for r, c in results:
                matching += r
                sum_cost += c

            end = time.time()
            iteration += 1
            print('Iteration\t%d\truntime\t%.4f\tdcmn\t%d'%(iteration, end - start, -sum_cost))

        return matching

