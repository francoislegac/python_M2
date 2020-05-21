"""Super appli baballe !!!

Usage: python balles.py
- clic gauche: faire grossir la boule la plus proche
- clic droit: faire rétrécir la boule
- touche i: inverser les vitesses
- flêches pour contrôler la boule bleue
- touche Esc: quitte l'appli
"""

import tkinter as tk
import numpy as np

class AppliBaballe(tk.Tk):
    def __init__(self, n):
        """Constructeur de l'application."""
        tk.Tk.__init__(self)
        # création et packing du canvas
        self.hauteur = 400
        self.largeur = 500
        self.canv = tk.Canvas(self, bg='snow2', height=self.hauteur,
            width=self.largeur)
        self.canv.pack()

        # coord balles
        self.z = np.zeros((n,2))
        self.z[:,0]+=self.largeur/2
        self.z[:,1]+=self.hauteur/2
        # rayon balles
        self.size = np.random.rand(n)*30+10
        # vitesses
        self.v = (np.random.rand(n,2)-.5)*4
        # création des balles
        self.baballe = [ self.canv.create_oval(self.z[i,0]-self.size[i]/2,
                                             self.z[i,1]-self.size[i]/2,
                                             self.z[i,0]+self.size[i]/2,
                                             self.z[i,1]+self.size[i]/2,
                                             width=0, fill='red')
                                             for i in range(n) ]
        self.canv.itemconfig(self.baballe[0],fill='blue')

        # binding des actions
        self.canv.bind("<Button-1>", self.incr)
        self.canv.bind("<Button-2>", self.incrbis)
        self.canv.bind("<Button-3>", self.decr)
        self.bind("<Escape>", self.stop)
        self.bind("i", self.inverse)
        self.bind("<Left>", self.gauche)
        self.bind("<Right>", self.droite)
        self.bind("<Up>", self.haut)
        self.bind("<Down>", self.bas)
        # lancer de l'animation
        self.move()

    def move(self):
        """Déplace les balles (appelée itérativement avec la méthode after)."""
        fl = self.z[:,0]<= self.size/2
        self.v[fl,0] *= -1; self.z[fl,0]= self.size[fl]/2
        fl = self.z[:,0]>= self.largeur- self.size/2
        self.v[fl,0] *= -1; self.z[fl,0]= self.largeur-self.size[fl]/2
        fl = self.z[:,1]<= self.size/2
        self.v[fl,1] *= -1; self.z[fl,1]= self.size[fl]/2
        fl = self.z[:,1]>= self.hauteur- self.size/2
        self.v[fl,1] *= - 1; self.z[fl,1]= self.hauteur-self.size[fl]/2

        self.z += self.v

        for i in range(len(self.baballe)):
            self.canv.coords(self.baballe[i], self.z[i,0]-self.size[i]/2,
                            self.z[i,1] -self.size[i]/2,
                             self.z[i,0]+self.size[i]/2, self.z[i,1]+self.size[i]/2)
        # rappel de move toutes les 1ms
        self.after(1, self.move)

    def gauche(self, e):
        self.v[0,0]+= -1/10

    def droite(self, e):
        self.v[0,0]+= 1/10

    def haut(self, e):
        self.v[0,1]+= -1/10

    def bas(self, e):
        self.v[0,1]+= 1/10

    def incr(self, mclick):
        """Augmente la taille de la baballe."""
        h=self.canv.find_closest(mclick.x,mclick.y)
        self.size[h[0]-1] += 1
        self.canv.itemconfig(h[0], fill='slate grey')

    def incrbis(self, lclick):
        """Augmente la taille de la baballe."""
        h=self.canv.find_closest(lclick.x,lclick.y)
        self.size[h[0]-1] +=1
        self.canv.itemconfig(h[0], fill='orange red')

    def decr(self, rclick):
        """Diminue la taille de la baballe."""
        h=self.canv.find_closest(rclick.x,rclick.y)
        self.size[h[0]-1] += -1
        self.canv.itemconfig(h[0], fill='red')

    def inverse(self, touche):
        self.v *= -1

    def stop(self, esc):
        """Quitte l'application."""
        self.quit()


if __name__ == "__main__":
    myapp = AppliBaballe(10)
    myapp.title("Billard")
    myapp.mainloop()
