# GABoost

This is a Python implementation of the paper:
> GABoost Is You All Need: Graph Alignment Boosting via Local Optimum Escape

## Datasets

The 6 datasets used in GABoost are contained in the `./dataset/` folder. 

- Douban, Movie and Megadiff changes are three datasets for the effectiveness experiments of GABoost. 

  Each of the Douban and Movie dataset contains a pair of heterogeneous graphs G0 and G1 as well as their ground-truth alignment.
  Megadiff changes dataset contains 10 pairs of graphs and their ground-truth alignments.

- Email-uni, Facebook, and DBLP are three datasets for the robustness experiments.

  Each of the datasets contains a real-world graph; based on it, we generate a set of graph pairs with different noise levels and numbers of vertex/edge types.

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

## Run

The GABoost code can be run in three mode:

- **Mode1 BOOST**: This mode refers to the GABoost algorithm in our paper, which is detailed in Algorithm 1.

  It inputs an initial alignment between graphs G0 and G1, and outputs a boosted one.

  The input initial alignment file should contains multiple lines. Each line represents an aligned node pair. The format is  `node_id1  node_id2`, and the seperator between `node_id1` and `node_id2` is `\t`.

  It should be noticed that the node id in initial alignment file should be consistent with the node id in the input graphs.

- **Mode2 SCMN**: This mode refers to the SCMN graph alignment method described in the Section V.A of our paper.

  It inputs two graphs G0 and G1, and outputs an alignment between them based on node's 1-hop information.

- **Mode3 SCMN+BOOST**: This mode refers to the combination of SCMN method and GABoost (GAB(SCMN)).

  In this mode, our code takes two graphs G0 and G1 as input, and then obtain an alignment based on SCMN, which is used as the initial alignment for GABoost. After that, our code outputs a GABoost-ed alignment of the SCMN alignment result.

   
