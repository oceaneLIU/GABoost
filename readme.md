# GABoost

This is a Python implementation of the paper:
> GABoost Is You All Need: Graph Alignment Boosting via Local Optimum Escape

## Datasets

The 6 datasets used in GABoost are contained in the `./dataset/` folder. 

- Douban, Movie and Megadiff changes are three datasets for the effectiveness experiments of GABoost.

  Each of the Douban and Movie dataset contains a pair of heterogeneous graphs G0 and G1 as well as their ground-truth alignment. Their file structure are as follows:

  ~~~
  dataset_name
    ├─ left_node_file  (node file of the graph G0)
    ├─ left_edge_file
    ├─ right_node_file
    ├─ left_edge_file
    └─ true_matching
  ~~~




   and the third dataset contains 10 pairs of graphs and their ground-truth alignments.
  
## Dependencies

## Run
