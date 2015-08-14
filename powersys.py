import numpy as np


def base(n,i,sgn=" 1"):
    if i < 0 or i >= n:
        return " 0 " * n
    else:
        return (" 0 " * i) + sgn + " " + (" 0 " * (n-1-i))

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

    def edge_expo(self,i,j):
        d = self.n - 1
        if 0 == i:
            v = " 0 " * d
        else:
            v = " 0 " * (i-1) + " 1 " + " 0 " * (d -i)
        if 0 == j:
            u = " 0 " * d
        else:
            u = " 0 " * (j-1) + " 1 " + " 0 " * (d -j)
        return v + u

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

    def supports(self):
        out = [str(self.m) + ' ' + str(self.m)]     # dimension and supports

        for i in range(1,self.n):   # for each node that is not the reference
            sz = len(self.G.neighbors(i)) + 1 # size of the supports
            out.append (str(sz) + " 1")
            out.append (str(sz) + " 1")

        for i in range(1,self.n):   # for each node that is not the reference
            fs = ['', self.edge_expo(0,0)]  # constant term
            gs = ['', self.edge_expo(0,0)]
            for j in self.G.neighbors(i):
                fs.append (self.edge_expo(i,j))
                gs.append (self.edge_expo(j,i))
            out.extend (fs)
            out.extend (gs)

        return "\n".join(out)

    def polytope(self):
        out = [str(self.m) + ' 1']     # dimension and supports

        P = set()
        P.add (self.edge_expo(0,0)) # constant term
        for i in range(1,self.n):   # for each node that is not the reference
            for j in self.G.neighbors(i):
                P.add (self.edge_expo(i,j))
                P.add (self.edge_expo(j,i))
        Ps = sorted(list(P), reverse=True)

        d = str(self.m)
        return  d + ' 1\n' + str(len(P)) + ' ' + d + "\n" + "\n".join(Ps)
