import sys
import imp
import getopt
import networkx as nx
import matplotlib.pyplot as plt
import powersys

to_draw = False

try:
    opts, args = getopt.getopt(sys.argv[1:], "h", ["help", "draw", "file", "supp", "sym"])
except getopt.GetoptError:
    usage()
    sys.exit(2)

for opt, arg in opts:
    if opt in ("-h", "--help"):
        usage()
    elif opt == "--draw":
        to_draw = True

if len(args) < 1:
    exit ("no graph is given\nUsage:\n  powergen GRAPH [PARAM1 PARAM2 ...]")

name = args[0]

try:
    f, fn, desc = imp.find_module(name)
    mod = imp.load_module ('generator', f, fn, desc)
    if len(args) - 1 < mod.argc:
        print 'Insufficient module options\n'
        print 'Module: ', name
        print 'options:', mod.args
        print 'size:   ', mod.size
    else:
        G = mod.create_graph(args[1:])
        if to_draw:
            nx.draw_graphviz(G)
            plt.show()
        P = powersys.PowerFlowSystem(G)
        print P.equations()
except ImportError, err:
    print 'Cannot load generator ' + name + ':', err
finally:
    f.close()

#G = nx.complete_graph(n)
