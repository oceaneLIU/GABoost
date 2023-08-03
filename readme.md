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
