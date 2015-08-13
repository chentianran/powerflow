import numpy as np


class PowerFlowSystem:

    def __init__(self, graph):
        self.fmt = "{0:.2f}"
        self.G  = graph;
        self.n = len(graph)                  # number of nodes
        self.m = 2*self.n - 2                 # number of variables
        self.v0 = np.random.randn()      # reference node
        self.Sr = np.random.randn(2*self.n)   # real parts
        self.Si = np.random.randn(2*self.n)   # imag parts
        for (x,y) in self.G.edges():
            self.G[x][y]['weight_r'] = np.random.randn()
            self.G[x][y]['weight_i'] = np.random.randn()

    def strf(self,x):
        return self.fmt.format(x)

    def cpx(self,r,i):
        if i < 0.0:
            return "(" + self.strf(r) +       self.strf(i) + "i)"
        else:
            return "(" + self.strf(r) + "+" + self.strf(i) + "i)"

    def vu(self, i, j):
        if i == 0:
            return "*" + self.strf(self.v0) + "*u" + str(j)
        elif j == 0:
            return "*" + self.strf(self.v0) + "*v" + str(i)
        else:
            return "*v" + str(i) + "*u" + str(j)

    def equations(self):
        out = ["{"]
        for i in range(1,self.n):
            fs = []
            gs = []
            for j in range(self.n):
                if self.G.has_edge(i,j):
                    e = self.G[i][j]
                    yf = self.cpx(e['weight_r'],+e['weight_i'])
                    yg = self.cpx(e['weight_r'],-e['weight_i'])
                    fs.append (yf + self.vu(i,j))
                    gs.append (yg + self.vu(j,i))
            Sf = self.cpx(self.Sr[i-1],+self.Si[i-1])
            Sg = self.cpx(self.Sr[i-1],-self.Si[i-1])
            out.append("  " + " + ".join(fs) + " - " + Sf + ";")
            out.append("  " + " + ".join(gs) + " - " + Sg + ";")
        out.append("}")
        return "\n".join(out)
