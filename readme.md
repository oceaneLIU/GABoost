# GABoost

This is a Python implementation of the paper:
> GABoost Is You All Need: Graph Alignment Boosting via Local Optimum Escape

## Datasets

- The datasets Douban, Movie and Megadiff changes used in GABoost are contained in the `./dataset/` folder. 

  Each of the Douban and Movie dataset contains a pair of heterogeneous graphs G0 and G1 as well as their ground-truth alignment.
  Megadiff changes dataset contains 4 folders. Each folder contains 10 pairs of graphs and their ground-truth alignments. 

- The file structure is as follows:
  ~~~
  dataset_name
    ├─ left_node_file  (node file of the graph G0)
    ├─ left_edge_file  (edge file of the graph G0)
    ├─ right_node_file (node file of the graph G1)
    ├─ left_edge_file  (edge file of the graph G1)
    └─ true_matching   (ground-truth alignment)
  ~~~
  
  Each line in the node file represents a node in the graph and its type. The format is `node_id  node_type`.
  Each line in the edge file represents a directed in the graph and its type. The format is `node_id1  node_id2  edge_type`. Note that if the graph is undirected, an undirected edge
  appears twice in the file, `node_id1  node_id2  edge_type` and `node_id2  node_id1  edge_type` respectively.
  Each line in true_matching file represents a ground-truth alignment node pair. The format is `node_id1  node_id2`.

   
  
## Dependencies

- python 3.9
- networkx 2.8.8
- numpy 1.23.4
- pyparsing 3.0.9
- scipy 1.9.3

## Run

The code can be run in three mode:

- **Mode1 GABoost**: This mode refers to the GABoost algorithm in our paper, which is detailed in Algorithm 1.

  It inputs an initial alignment between graphs G0 and G1, and outputs a boosted one.

  In this mode, there are 7 input arguments:

  - input_initial_alignment: The path of input initial alignment file. The input initial alignment file should contains multiple lines. Each line represents an aligned node pair. The format is `node_id1  node_id2`, the seperator between `node_id1` and `node_id2` is `\t`.

    It should be noticed that the node id in initial alignment file should be consistent with the node id in the input graphs.

  - input_g0_node: The path of node file of the graph G0.
 
  - input_g0_edge: The path of edge file of the graph G0.
 
  - input_g1_node: The path of node file of the graph G1.
 
  - input_g1_edge: The path of edge file of the graph G1.

  - save_output_alignment: Output alignment save path. If None, output alignment result is not saved.

  - ground_truth_alignment: Ground-truth alignment file path. If it is None, the metrics accuracy (ACC), mean average precision (MAP), edge correctness (EC) and induced conserved structure (ICS) will not be computed.
 
  For example:
  ~~~
  python runGABoost.py --mode GABoost --input_g0_node ./dataset/movie/left_node_file --input_g0_edge ./dataset/movie/left_edge_file --input_g1_node ./dataset/movie/right_node_file --input_g1_edge ./dataset/movie/right_edge_file --input_initial_alignment ./dataset/movie/scmn_output_alignment --ground_truth_alignment ./dataset/movie/true_matching --save_output_alignment ./dataset/movie/gaboost_output_alignment
  ~~~

- **Mode2 SCMN**: This mode refers to the SCMN graph alignment method described in the Section V.A of our paper.

  It inputs two graphs G0 and G1, and outputs an alignment between them based on node's 1-hop information.

  In this mode, there are 6 input arguments:

  - input_g0_node: The path of node file of the graph G0.
 
  - input_g0_edge: The path of edge file of the graph G0.
 
  - input_g1_node: The path of node file of the graph G1.
 
  - input_g1_edge: The path of edge file of the graph G1.

  - save_output_alignment: Output alignment save path. If None, output alignment result is not saved.

  - ground_truth_alignment: Ground-truth alignment file path. If it is None, the metrics accuracy (ACC), mean average precision (MAP), edge correctness (EC) and induced conserved structure (ICS) will not be computed.
  For example:
  ~~~
  python runGABoost.py --mode SCMN --input_g0_node ./dataset/movie/left_node_file --input_g0_edge ./dataset/movie/left_edge_file --input_g1_node ./dataset/movie/right_node_file --input_g1_edge ./dataset/movie/right_edge_file --ground_truth_alignment ./dataset/movie/true_matching --save_output_alignment ./dataset/movie/scmn_output_alignment
  ~~~
  
- **Mode3 SCMN+GABoost**: This mode refers to the combination of SCMN method and GABoost (GAB(SCMN)).

  In this mode, our code takes two graphs G0 and G1 as input, and then obtain an alignment based on SCMN, which is used as the initial alignment for GABoost. After that, our code outputs a GABoost-ed alignment of the SCMN alignment result.

  In this mode, there are 6 input arguments:

  - input_g0_node: The path of node file of the graph G0.
 
  - input_g0_edge: The path of edge file of the graph G0.
 
  - input_g1_node: The path of node file of the graph G1.
 
  - input_g1_edge: The path of edge file of the graph G1.

  - save_output_alignment: Output alignment save path. If None, output alignment result is not saved.

  - ground_truth_alignment: Ground-truth alignment file path. If it is None, the metrics accuracy (ACC), mean average precision (MAP), edge correctness (EC) and induced conserved structure (ICS) will not be computed.

  For example:
  ~~~
  python runGABoost.py --mode SCMN+GABoost --input_g0_node ./dataset/movie/left_node_file --input_g0_edge ./dataset/movie/left_edge_file --input_g1_node ./dataset/movie/right_node_file --input_g1_edge ./dataset/movie/right_edge_file --ground_truth_alignment ./dataset/movie/true_matching --save_output_alignment ./dataset/movie/scmn_gaboost_output_alignment
  ~~~
