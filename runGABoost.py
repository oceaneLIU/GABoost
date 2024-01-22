import os
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


def main(args, cpu_num):
    # read input
    start = time.time()
    graph0 = read_graph(args.input_g0_node, args.input_g0_edge)
    graph1 = read_graph(args.input_g1_node, args.input_g1_edge)
    end = time.time()
    print('Input graphs reading finish, reading time=%.4f s' % (end - start))

    # running algorithm
    start = time.time()
    if args.mode == 'GABoost':
        initial_alignment = read_matching(args.input_initial_alignment)
        alg = GABoost(graph0, graph1, initial_alignment)
        output_alignment = alg.get_matching(cpu_num)

    if args.mode == 'SCMN':
        alg = SCMN(graph0, graph1)
        output_alignment = alg.get_matching(cpu_num)

    if args.mode == 'SCMN+GABoost':
        alg0 = SCMN(graph0, graph1)
        scmn_alignment = alg0.get_matching(cpu_num)
        alg = GABoost(graph0, graph1, scmn_alignment)
        output_alignment = alg.get_matching(cpu_num)
    end = time.time()

    # save
    if args.save_output_alignment is not None:
        with open(args.save_output_alignment, 'w') as f:
            for v, u in output_alignment:
                f.write(str(v)+'\t'+str(u)+'\n')


    # evaluation
    if args.ground_truth_alignment is not None:
        gt = read_matching(args.ground_truth_alignment)

        ACC = accuracy(output_alignment, gt)
        MAP = mean_average_precision(gt, graph0, graph1, dis=args.mode, predict_alignment=output_alignment)
        EC = edge_correctness(output_alignment, graph0, graph1)
        ICS = induced_conserved_structure(output_alignment, graph0, graph1)

        print('---------------Final result---------------')
        print('mode = ', args.mode)
        print('input_g0_node = ', args.input_g0_node)
        print('input_g0_edge = ', args.input_g0_edge)
        print('input_g1_node = ', args.input_g1_node)
        print('input_g1_edge = ', args.input_g1_edge)
        print('input_initial_alignment = ', args.input_initial_alignment)
        print('ground_truth_alignment = ', args.ground_truth_alignment)
        print('save_output_alignment = ', args.save_output_alignment)
        print('Alignment accuracy(ACC) = %.4f' % ACC)
        print('Mean average precision(MAP) = %.4f' % MAP)
        print('Edge correctness(EC) = %.4f' % EC)
        print('Induced conserved structure(ICS) = %.4f' % ICS)
        print('Algorithm running time = %.4f' % (end-start))


if __name__ == '__main__':
    cpu_num = os.cpu_count()
    args = parse_args()
    main(args, cpu_num)
