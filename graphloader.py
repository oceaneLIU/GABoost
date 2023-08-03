import networkx as nx


def read_graph(node_path, edge_path):
    node_file = open(node_path, 'r')
    line = node_file.readline()
    graph = nx.DiGraph()
    while line:
        node_id = int(line.strip('\n').split('\t')[0])
        node_type = int(line.strip('\n').split('\t')[1])
        graph.add_node(node_id, type=node_type)
        line = node_file.readline()
    node_file.close()

    edge_file = open(edge_path, 'r')
    line = edge_file.readline()
    while line:
        node_id1 = int(line.strip('\n').split('\t')[0])
        node_id2 = int(line.strip('\n').split('\t')[1])
        edge_type = int(line.strip('\n').split('\t')[2])
        graph.add_edge(node_id1, node_id2, type=edge_type)
        line = edge_file.readline()
    edge_file.close()

    return graph


def read_matching(matching_path):
    mat = []
    file = open(matching_path, 'r')
    line = file.readline()
    while line:
        v = int(line.strip('\n').split('\t')[0])
        u = int(line.strip('\n').split('\t')[1])
        mat.append((v, u))
        line = file.readline()
    file.close()
    return mat
