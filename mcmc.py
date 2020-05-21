# importing pyplot and image from matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as img
import matplotlib.animation as animation
import numpy as np

# reading png image file
im = img.imread('Graphyti.png')

# affichage de l'image initiale
plt.imshow(im)
plt.show()

fig = plt.figure(figsize=(10, 7), frameon=False)
ax = plt.subplot(111, frameon=False)


nb=0
p=1; q=1

def animate(i,im,im2,be,si):
    m=50000
    x = np.random.randint(1,im2.shape[0]-1, size=(m,))
    y = np.random.randint(1,im2.shape[1]-1, size=(m,))
    # Calcul des voisins
    dx = np.array([-1,0,1,-1,0,1,-1,0,1])
    dy = np.array([-1,-1,-1,0,0,0,1,1,1])
    fx = x[:,np.newaxis] + dx[np.newaxis,:]
    fy = y[:,np.newaxis] + dy[np.newaxis,:]

    pith = -(be* np.abs(im2[fx[:,:], fy[:,:],:]\
- im2[x[:,np.newaxis], y[:,np.newaxis],:])**p).sum(axis=(1,2))
    pith += -(np.abs((im2[x,y,:]-im[x,y,:])/si)**q).sum(axis=1)

    coul = np.random.rand(m,3) # nouvelle couleur proposée

    pixi = -( be*np.abs(im2[fx[:,:], fy[:,:],:]\
- coul[:,np.newaxis,:])**p).sum(axis=(1,2))
    pixi += -(np.abs((coul[:,:]-im[x,y,:])/si)**q).sum(axis=1)

    rho = np.minimum(1, np.exp(pixi - pith))
    flag = np.random.rand(m) <= rho
    im2[x[flag],y[flag],:]=coul[flag,:]
    global nb
    nb+=np.sum(flag)

    ax.cla()
    ax.imshow(np.minimum(1,np.maximum(0,im2)))
    ax.axis('off')
    ax.set_title("nb {}".format(nb))

im2 = np.copy(im)
be = 2
si = .1
ani = animation.FuncAnimation(fig, animate, range(1, 100000),
                              interval=10, fargs=(im,im2,be,si),repeat=False)
plt.show()
