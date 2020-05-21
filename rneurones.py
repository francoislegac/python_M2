import numpy as np

class rn:
    def __init__(self,shape):
        self.shape = shape # une liste qui contient les N_l, l=0,...,L-1
        self.X= [ np.zeros(n) for n in shape]
        self.X.append(np.zeros((1,)))
        aux = list(shape)
        aux.append(1)
        # initialisation au hasard de a et b
        self.b = [ np.random.rand(n)/n for n in aux[1:]]
        self.a = [ (np.random.random_sample((aux[ell+1],aux[ell]))-.5)/np.sqrt(aux[ell]/12) \
for ell in range(len(shape))]

    def CalculSortie(self):
        for ell in range(len(self.X)-2):
            self.X[ell+1][:] = np.maximum(0,self.b[ell] + self.a[ell] @ self.X[ell])
        self.X[-1] = self.b[-1] + self.a[-1] @ self.X[-2]

    def Retro(self,g, pas):
        grad = -2*pas*(self.X[-1]-g)
        for ell in range(len(self.X)-2,-1,-1):
            aux = np.copy(grad)
            if ell < (len(self.X)-2):
                aux *= (self.X[ell+1]>0)
            grad = (self.a[ell]*grad[:,np.newaxis]).sum(axis=0)
            self.b[ell] += aux
            self.a[ell] += aux[:,np.newaxis]*self.X[ell][np.newaxis,:]


n = 100
m=50; truc = rn([n,m,m])
pas = 5e-4
nbrep = 10000

for k in range(100):
    se = 0; seop=0
    for rep in range(nbrep):
        theta = (np.random.rand()-.5)*np.pi*2
        g = np.cos(theta)
        truc.X[0] = np.random.randn(n) + theta
        truc.CalculSortie()
        se += (truc.X[-1]-g)**2
        seop += (np.cos(np.mean(truc.X[0]))-g)**2
        truc.Retro(g,pas)
    print(np.sqrt(se /nbrep),' vs ', np.sqrt(seop/nbrep))
