import networkx as nx

argc = 1
args = 'leves'
size = 'size of a complete binary tree'

def create_graph(opts):
    n = int(opts[0])
    return nx.balanced_tree(2,n)
