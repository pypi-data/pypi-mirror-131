# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 12:32:50 2021

@author: e4hgurge
"""
import math
import numpy as np
import matplotlib.pyplot as plt


DEBUG=False

def skiplines(fp,n, show=False):
    for i in range(0, n):
        line=fp.readline()
        if show: print(line)
    return line

def zonenames(idffile):
    sa=[]
    with open(idffile) as fp:
        while True:
            line=fp.readline()
            if not line: return sa
            if "," in line:
                a=line.split(",")
                if a[0].lstrip()=="Zone":
                    line=fp.readline()
                    a=line.split(",")
                    sa.append(a[0].strip())
                
    

def zonesurfaces(idffile, zonename,epver):
    surfacearray=[]
    if DEBUG: print(idffile, zonename)
    with open(idffile) as fp:
        while True:
            line=fp.readline()
            if not line: return surfacearray
            if "," in line:
                a=line.split(",")
                if a[0].lstrip()=="BuildingSurface:Detailed":
                    if DEBUG: print(a[0], end="")
                    line=skiplines(fp, 4)
                    a=line.split(",")
                    if DEBUG: print(a[0], end="")
                    if a[0].lstrip()==zonename:
                        if epver==6:
                            nskip=7
                        else:
                            nskip=6
                        a=skiplines(fp, nskip, show=DEBUG).split(",")
                        n=int(a[0])
                        if DEBUG: print("Number of vertices = %d"%n, end="")
                        surface=np.zeros([n, 3])
                        for i in range(0, n):
                            line=fp.readline()
                            a=line.split(",")
                            for j in range(0, 3):
                                if ";" in a[j]:
                                    s=a[j].split(";")[0]
                                else:
                                    s=a[j]
                                surface[i,j]=float(s.strip())
                        surfacearray.append(surface)
            
                        # print(surface)
def plotsurface(ax,surface, lc, name=""):
    a=surface.ravel()
    x=a[0:12:3]
    y=a[1:12:3]
    z=a[2:12:3]
    
    ax.plot(np.append(x, x[0]), np.append(y, y[0]), np.append(z, z[0]), lc, label="Wall")
    if name !="":
        ax.legend()
    
def plotzone(idffile, zonename, ax, lc, epver):
    sa=zonesurfaces(idffile, zonename, epver)
    for surface in sa:
        plotsurface(ax, surface, lc)

def idfplot(idffile, filename="", epver=5):
    za=zonenames(idffile)           
    fig=plt.figure()
    ax=fig.add_subplot(projection='3d')
    for z in za:
        plotzone(idffile, z, ax, 'k', epver)
    if filename=="":
        plt.show()
    else:
        fig.savefig(filename)
    
            
if __name__ == "__main__":
    import os
    examplefolder="/Users/Halim/work/eplus/idf/ep_96_examples"
    examplefile="EMSPlantLoopOverrideControl.idf"
    examplefile="1ZoneUncontrolled.idf"
    # examplefile="PythonPluginWindowShadeControl.idf"
    idffile=os.path.join(examplefolder, examplefile)
    DEBUG=False
    za=zonenames(idffile)           
    fig=plt.figure()
    ax=fig.add_subplot(projection='3d')
    n=len(za)
    lca=["k", "b", "r", "g", "m", "y", "c", "k--", "b--", "r--", "g--"]

    for i in range(0, n):
        plotzone(idffile, za[i], ax, lca[i%(len(lca))],6)
        print(za[i])
        i+=1
    plt.show()
        
    

#def plotbuildingsurface(fp, ax, surfacename)


# C5_1=np.array([
#       [3.7,11.6,2.4],  # X,Y,Z ==> Vertex 1 {m}
#     [3.7,3.7,2.4],  # X,Y,Z ==> Vertex 2 {m}
#     [26.8,3.7,2.4],  # X,Y,Z ==> Vertex 3 {m}
#     [26.8,11.6,2.4]  # X,Y,Z ==> Vertex 4 {m}
#       ])

# fig=plt.figure()
# ax=fig.add_subplot(projection='3d')
# a=C5_1.ravel()
# x=a[0:12:3]
# y=a[1:12:3]
# z=a[2:12:3]

# ax.plot(np.append(x, x[0]), np.append(y, y[0]), np.append(z, z[0]), label="Wall")
# ax.legend()
# plt.show()

