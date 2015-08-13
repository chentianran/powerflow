import networkx as nx

argc = 2
args = 'n1 n2'
size = 'n1 + n2'

def create_graph(opts):
    n1 = int(opts[0])
    n2 = int(opts[1])
    return nx.complete_bipartite_graph(n1,n2)
