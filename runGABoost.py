import time
import argparse
import multiprocessing as mp
from metrics import *
import sys
from graphloader import *
from algorithm.SCMN import SCMN
from algorithm.GABoost import GABoost
import networkx as nx
import numpy as np
import threading
import multiprocessing as mp
from functools import partial
from scipy.optimize import linear_sum_assignment

def parse_args():
    parser = argparse.ArgumentParser(description="Run GABoost.")
    parser.add_argument('--mode', help='Choose from (1)GABoost (2)SCMN (3)SCMN+GABoost')
    parser.add_argument('--input_g0_node', type=str, default='./dataset/douban/left_node_file')
    parser.add_argument('--input_g0_edge', type=str, default='./dataset/douban/left_edge_file')
    parser.add_argument('--input_g1_node', type=str, default='./dataset/douban/right_node_file')
    parser.add_argument('--input_g1_edge', type=str, default='./dataset/douban/right_edge_file')
    parser.add_argument('--save_output_alignment', type=str, default='./dataset/douban/output_alignment')
    parser.add_argument('--ground_truth_alignment', type=str, default='./dataset/douban/true_matching')
    parser.add_argument('--input_initial_alignment', type=str, default=None)
    return parser.parse_args()


def main(mode, input_g0_node, input_g0_edge, input_g1_node, input_g1_edge, input_initial_alignment, ground_truth_alignment, save_output_alignment, cpu_num):
    # read input
    start = time.time()
    graph0 = read_graph(input_g0_node, input_g0_edge)
    graph1 = read_graph(input_g1_node, input_g1_edge)
    end = time.time()
    print('Input graphs reading finish, reading time=%.4f s' % (end - start))

    # running algorithm
    start = time.time()
    if mode == 'GABoost':
        initial_alignment = read_matching(input_initial_alignment)
        alg = GABoost(graph0, graph1, initial_alignment)
        output_alignment = alg.get_matching(cpu_num-1)

    if mode == 'SCMN':
        alg = SCMN(graph0, graph1)
        output_alignment = alg.get_matching(cpu_num-1)

    if mode == 'SCMN+GABoost':
        alg0 = SCMN(graph0, graph1)
        scmn_alignment = alg0.get_matching(cpu_num-1)
        alg = GABoost(graph0, graph1, scmn_alignment)
        output_alignment = alg.get_matching(cpu_num-1)
    end = time.time()

    # save
    if save_output_alignment is not None:
        with open(save_output_alignment, 'w') as f:
            for v, u in output_alignment:
                f.write(str(v)+'\t'+str(u)+'\n')


    # evaluation
    if ground_truth_alignment is not None:
        gt = read_matching(ground_truth_alignment)

        ACC = accuracy(output_alignment, gt)

        print('---------------Final result---------------')
        print('mode = ', mode)
        print('input_g0_node = ', input_g0_node)
        print('input_g0_edge = ', input_g0_edge)
        print('input_g1_node = ', input_g1_node)
        print('input_g1_edge = ', input_g1_edge)
        print('input_initial_alignment = ', input_initial_alignment)
        print('ground_truth_alignment = ', ground_truth_alignment)
        print('save_output_alignment = ', save_output_alignment)
        print('Alignment accuracy = %.4f' % ACC)
        print('Algorithm running time = %.4f' % (end-start))


if __name__ == '__main__':
    mp.freeze_support()
    cpu_num = 2
    args = [None for i in range(0, 8)]
    args = sys.argv[1:]
    mode = args[0]
    input_g0_node = args[1]
    input_g0_edge = args[2]
    input_g1_node = args[3]
    input_g1_edge = args[4]
    input_initial_alignment = args[5]
    ground_truth_alignment = args[6]
    save_output_alignment = args[7]
    main(mode, input_g0_node, input_g0_edge, input_g1_node, input_g1_edge,
         input_initial_alignment, ground_truth_alignment, save_output_alignment, cpu_num)
