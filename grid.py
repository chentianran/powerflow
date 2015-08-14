import networkx as nx

argc = 2
args = 'n1 n2'
size = 'n1 x n2'

def create_graph(opts):
    n1 = int(opts[0])
    n2 = int(opts[1])
    return nx.convert_node_labels_to_integers(nx.grid_2d_graph(n1,n2))
