import time
import argparse
import multiprocessing as mp
from metrics import *
from graphloader import *
from algorithm.SCMN import *
from algorithm.GABoost import *


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
        output_alignment = alg.get_matching(cpu_num-1)

    if args.mode == 'SCMN':
        alg = SCMN(graph0, graph1)
        output_alignment = alg.get_matching(cpu_num-1)

    if args.mode == 'SCMN+GABoost':
        alg0 = SCMN(graph0, graph1)
        scmn_alignment = alg0.get_matching(cpu_num-1)
        alg = GABoost(graph0, graph1, scmn_alignment)
        output_alignment = alg.get_matching(cpu_num-1)
    end = time.time()

    # save
    if args.save_output_alignment is not None:
        with open(args.save_output_alignment, 'w') as f:
            for v, u in output_alignment:
                f.write(str(v)+'\t'+str(u)+'\n')

    # evaluation
    if args.ground_truth_alignment is not None:
        ground_truth_alignment = read_matching(args.ground_truth_alignment)

        ACC = accuracy(output_alignment, ground_truth_alignment)
        if args.mode == 'SCMN':
            ctx1 = alg.basic_static_node_context(graph0)
            ctx2 = alg.basic_static_node_context(graph1)
            dis = 'scmn'
        else:
            ctx1 = alg.dynamic_vertex_context(graph0, 'left', output_alignment)
            ctx2 = alg.dynamic_vertex_context(graph1, 'right', output_alignment)
            dis = 'dcmn'
        MAP = mean_average_precision(ground_truth_alignment, ctx1, ctx2, dis=dis)
        EC = edge_correctness(output_alignment, graph0, graph1)
        ICS = induced_conserved_structure(output_alignment, graph0, graph1)

        print('-'*50)
        print(' '.join(f'{k}={v}' for k, v in vars(args).items()))
        print('Accuracy = %.4f' % ACC)
        print('Mean average precision = %.4f' % MAP)
        print('Edge correctness = %.4f' % EC)
        print('Induced conserved structure = %.4f' % ICS)
        print('Process time = %.4f' % (end-start))


if __name__ == "__main__":
    args = parse_args()
    cpu_num = mp.cpu_count()
    main(args, cpu_num)


