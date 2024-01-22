# GABoost

This is a Python implementation of the paper:
> GABoost: Graph Alignment Boosting via Local Optimum Escape

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

## Requirements

- networkx==3.1
- numpy==1.25.2
- scipy==1.11.1

## Run
We provide a python file `runGABoost.py` as well as two executable binary version `runGABoost_mac` and `runGABoost_win.exe` of GABoost for Mac and Windows, respectively. 
There are 8 input arguments for GABoost:

  - mode: The code can be run in three mode: `SCMN`, `GABoost`, and `SCMN+GABoost`.
    - `SCMN`: The SCMN graph alignment method described in the Section V.A of our paper.
    - `GABoost`: The GABoost algorithm in our paper, which is detailed in Algorithm 1.
    - `SCMN+GABoost`: The combination of SCMN method and GABoost (GAB(SCMN)).
      
  - input_g0_node: The path of node file of the graph G0.
 
  - input_g0_edge: The path of edge file of the graph G0.
 
  - input_g1_node: The path of node file of the graph G1.
 
  - input_g1_edge: The path of edge file of the graph G1.

  - input_initial_alignment:  The path of input initial alignment file. Only required for `GABoost` mode. For `SCMN` and `SCMN+GABoost` mode, this argument should be set to None. The input initial alignment file should contains multiple lines. Each line represents an aligned node pair. The format is `node_id1  node_id2`, the seperator between `node_id1` and `node_id2` is `\t`.

  - ground_truth_alignment: Ground-truth alignment file path. If it is None, the alignment accuracy (ACC) can not be computed.

  - save_output_alignment: Output alignment save path. If None, output alignment result is not saved.

### Running example in `SCMN` mode

- On douban dataset

  runGABoost.py
  ~~~
  python runGABoost.py --mode SCMN --input_g0_node ./dataset/douban/left_node_file --input_g0_edge ./dataset/douban/left_edge_file --input_g1_node ./dataset/douban/right_node_file --input_g1_edge ./dataset/douban/right_edge_file --save_output_alignment ./dataset/douban/scmn_output_alignment --ground_truth_alignment ./dataset/douban/true_matching
  ~~~
  
  Mac
  ~~~
  ./runGABoost_mac SCMN ./dataset/douban/left_node_file ./dataset/douban/left_edge_file ./dataset/douban/right_node_file ./dataset/douban/right_edge_file None ./dataset/douban/true_matching ./dataset/douban/scmn_output_alignment
  ~~~

  Windows
  ~~~
  runGABoost_win SCMN ./dataset/douban/left_node_file ./dataset/douban/left_edge_file ./dataset/douban/right_node_file ./dataset/douban/right_edge_file None ./dataset/douban/true_matching ./dataset/douban/scmn_output_alignment
  ~~~
- On movie dataset

  runGABoost.py
  ~~~
  python runGABoost.py --mode SCMN --input_g0_node ./dataset/movie/left_node_file --input_g0_edge ./dataset/movie/left_edge_file --input_g1_node ./dataset/movie/right_node_file --input_g1_edge ./dataset/movie/right_edge_file --save_output_alignment ./dataset/movie/scmn_output_alignment --ground_truth_alignment ./dataset/movie/true_matching
  ~~~
  
  Mac
  ~~~
  ./runGABoost_mac SCMN ./dataset/movie/left_node_file ./dataset/movie/left_edge_file ./dataset/movie/right_node_file ./dataset/movie/right_edge_file None ./dataset/movie/true_matching ./dataset/movie/scmn_output_alignment
  ~~~

  Windows
  ~~~
  runGABoost_win SCMN ./dataset/movie/left_node_file ./dataset/movie/left_edge_file ./dataset/movie/right_node_file ./dataset/movie/right_edge_file None ./dataset/movie/true_matching ./dataset/movie/scmn_output_alignment
  ~~~

### Running example in `GABoost` mode

- On douban dataset

  runGABoost.py
  ~~~
  python runGABoost.py --mode GABoost --input_g0_node ./dataset/douban/left_node_file --input_g0_edge ./dataset/douban/left_edge_file --input_g1_node ./dataset/douban/right_node_file --input_g1_edge ./dataset/douban/right_edge_file --save_output_alignment ./dataset/douban/gaboost_output_alignment --ground_truth_alignment ./dataset/douban/true_matching --input_initial_alignment ./dataset/douban/scmn_output_alignment
  ~~~
  
  Mac
  ~~~
  ./runGABoost_mac GABoost ./dataset/douban/left_node_file ./dataset/douban/left_edge_file ./dataset/douban/right_node_file ./dataset/douban/right_edge_file ./dataset/douban/scmn_output_alignment ./dataset/douban/true_matching ./dataset/douban/gaboost_output_alignment
  ~~~

  Windows
  ~~~
  runGABoost_win GABoost ./dataset/douban/left_node_file ./dataset/douban/left_edge_file ./dataset/douban/right_node_file ./dataset/douban/right_edge_file ./dataset/douban/scmn_output_alignment ./dataset/douban/true_matching ./dataset/douban/gaboost_output_alignment
  ~~~
- On movie dataset
  
  runGABoost.py
  ~~~
  python runGABoost.py --mode GABoost --input_g0_node ./dataset/movie/left_node_file --input_g0_edge ./dataset/movie/left_edge_file --input_g1_node ./dataset/movie/right_node_file --input_g1_edge ./dataset/movie/right_edge_file --save_output_alignment ./dataset/movie/gaboost_output_alignment --ground_truth_alignment ./dataset/movie/true_matching --input_initial_alignment ./dataset/movie/scmn_output_alignment
  ~~~
  
  Mac
  ~~~
  ./runGABoost_mac GABoost ./dataset/movie/left_node_file ./dataset/movie/left_edge_file ./dataset/movie/right_node_file ./dataset/movie/right_edge_file ./dataset/movie/scmn_output_alignment ./dataset/movie/true_matching ./dataset/movie/gaboost_output_alignment
  ~~~

  Windows
  ~~~
  runGABoost_win GABoost ./dataset/movie/left_node_file ./dataset/movie/left_edge_file ./dataset/movie/right_node_file ./dataset/movie/right_edge_file ./dataset/movie/scmn_output_alignment ./dataset/movie/true_matching ./dataset/movie/gaboost_output_alignment
  ~~~

### Running example in `SCMN+GABoost` mode

- On douban dataset

  runGABoost.py
  ~~~
  python runGABoost.py --mode SCMN+GABoost --input_g0_node ./dataset/douban/left_node_file --input_g0_edge ./dataset/douban/left_edge_file --input_g1_node ./dataset/douban/right_node_file --input_g1_edge ./dataset/douban/right_edge_file --save_output_alignment ./dataset/douban/scmn+gaboost_output_alignment --ground_truth_alignment ./dataset/douban/true_matching
  ~~~
  
  Mac
  ~~~
  ./runGABoost_mac SCMN+GABoost ./dataset/douban/left_node_file ./dataset/douban/left_edge_file ./dataset/douban/right_node_file ./dataset/douban/right_edge_file None ./dataset/douban/true_matching ./dataset/douban/scmn+gaboost_output_alignment
  ~~~

  Windows
  ~~~
  runGABoost_win SCMN+GABoost ./dataset/douban/left_node_file ./dataset/douban/left_edge_file ./dataset/douban/right_node_file ./dataset/douban/right_edge_file None ./dataset/douban/true_matching ./dataset/douban/scmn+gaboost_output_alignment
  ~~~
  
- On movie dataset

  runGABoost.py
  ~~~
  python runGABoost.py --mode SCMN+GABoost --input_g0_node ./dataset/movie/left_node_file --input_g0_edge ./dataset/movie/left_edge_file --input_g1_node ./dataset/movie/right_node_file --input_g1_edge ./dataset/movie/right_edge_file --save_output_alignment ./dataset/movie/scmn+gaboost_output_alignment --ground_truth_alignment ./dataset/movie/true_matching
  ~~~
  
  Mac
  ~~~
  ./runGABoost_mac SCMN+GABoost ./dataset/movie/left_node_file ./dataset/movie/left_edge_file ./dataset/movie/right_node_file ./dataset/movie/right_edge_file None ./dataset/movie/true_matching ./dataset/movie/scmn+gaboost_output_alignment
  ~~~

  Windows
  ~~~
  runGABoost_win SCMN+GABoost ./dataset/movie/left_node_file ./dataset/movie/left_edge_file ./dataset/movie/right_node_file ./dataset/movie/right_edge_file None ./dataset/movie/true_matching ./dataset/movie/scmn+gaboost_output_alignment
  ~~~

  
