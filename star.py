import networkx as nx

argc = 1
args = 'nodes'
size = 'nodes'

def create_graph(opts):
    n = int(opts[0])
    return nx.star_graph(n)
