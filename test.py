import cv2
import random
import numpy as np
import matplotlib as mp
from scipy.ndimage import gaussian_filter


# reading image
I=cv2.imread('grain.png')

print('Enter sigma,k and min_scale\n')
sigma=input()
sig=float(sigma)
cc=input()
cc=float(cc)
min_scale=input()
ms=float(min_scale)
md=input()
md=float(md)
#cv2.imshow('image',I)

Ir = gaussian_filter(I[:,:,0],sig)
Ig = gaussian_filter(I[:,:,1],sig)
Ib = gaussian_filter(I[:,:,2],sig)
I[:,:,0]=Ir
I[:,:,1]=Ig
I[:,:,2]=Ib
Ii=I
print(I.min()," ",I.max)
height=np.size(I,0)
width=np.size(I,1)
n=height*width


#initialzing edges
class ej:
    # a and b are end vertices and w is the weight connecting the two as per pixel adjacency 
    a=0
    b=0
    w=0.2
    def __init__(self, number):
        self.number = number


edge = []
m=4*n
for i in range(0,m):
    edge.append(ej(i))

#updating the edge with pair of neighbour pixels
z=0
for x in range(0,height):
    for y in range(0,width):
        num=x*width+y
        if(x<height-1):
            edge[z].a=num
            edge[z].b=num+width
            res=pow(float(I[x+1][y][0])-float(I[x][y][0]),2)+pow(float(I[x+1][y][1])-float(I[x][y][1]),2)+pow(float(I[x+1][y][2])-float(I[x][y][2]),2)
            edge[z].w=pow(res,0.5)
            z=z+1
            
        if(y<width-1):
            edge[z].a=num
            edge[z].b=num+1
            res=pow(float(I[x][y+1][0])-float(I[x][y][0]),2)+pow(float(I[x][y+1][1])-float(I[x][y][1]),2)+pow(float(I[x][y+1][2])-float(I[x][y][2]),2)
            edge[z].w=pow(res,0.5)
            z=z+1

        if(x<height-1 and y<width-1):
            edge[z].a=num
            edge[z].b=num+width+1
            res=pow(float(I[x+1][y+1][0])-float(I[x][y][0]),2)+pow(float(I[x+1][y+1][1])-float(I[x][y][1]),2)+pow(float(I[x+1][y+1][2])-float(I[x][y][2]),2)
            edge[z].w=pow(res,0.5)
            z=z+1
            
        if(x<height-1 and y>0):
            edge[z].a=num
            edge[z].b=num+width-1
            res=pow(float(I[x+1][y-1][0])-float(I[x][y][0]),2)+pow(float(I[x+1][y-1][1])-float(I[x][y][1]),2)+pow(float(I[x+1][y-1][2])-float(I[x][y][2]),2)
            edge[z].w=pow(res,0.5)
            z=z+1

l=z

#sorting edges
edge.sort(key = lambda x:x.w)


#initializing disjoint sets

class dis_set:
    rank=0
    p=0
    size=0
    iw=0.0
    def __init__(self, number):
        self.number = number

def find(val):
    if(arr[val].p==val):
        return val
    x=find(arr[val].p)
    arr[val].p=x
    return x
def join(val1,val2,wt):
    x=find(val1)
    y=find(val2)
    temp=max(arr[x].iw,arr[y].iw);
    arr[x].size=arr[x].size+arr[y].size
    arr[y].size=arr[x].size
    if(arr[x].rank>arr[y].rank):
        arr[y].p=x
        arr[x].iw=max(temp,wt);
    else:
        arr[x].p=y
        arr[y].iw=max(temp,wt);
        if(arr[x].rank==arr[y].rank):
            arr[y].rank=arr[y].rank+1


arr = []
ww=np.zeros([n],dtype=np.float)
for i in range(0,n):
    arr.append(dis_set(i))

for i in range(0,n):
    arr[i].rank=0
    arr[i].p=i
    arr[i].size=1
    arr[i].iw=float(cc)
    ww[i]=0

# Iterating for each edge


# Internal difference in the set 
def MInt(r,h):
    #r=arr[x].size
    if(r<19999999999):
        r=h/r
    else:
        r=h/19999999999
    return r

for i in range(0,l):
    p1=edge[i].a
    p2=edge[i].b
    dif=edge[i].w
    # find internal variance Int(p1,p2) and Diff(p1,p2) then compare bwtween them for joining them further
    x=find(p1)
    y=find(p2)
    if(x==y):
        continue
    g=arr[x].size
    h=arr[y].size
    if(dif<=arr[x].iw and dif <= arr[y].iw or dif<md):
        join(x,y,dif)
        ww[x]=dif
        ww[y]=ww[x]
        arr[x].iw=dif+MInt(g+h,cc)
        arr[y].iw=dif+MInt(g+h,cc)

for i in range(0,l):
    p1=edge[i].a
    p2=edge[i].b
    dif=edge[i].w
    # find internal variance Int(p1,p2) and Diff(p1,p2) then compare bwtween them for joining them further
    x=find(p1)
    y=find(p2)
    if(x==y):
        continue
    g=arr[x].size
    h=arr[y].size
    if(g<ms or h<ms):
        join(x,y,dif)
        ww[x]=max(dif,ww[x],ww[y])
        ww[y]=ww[x]
        arr[x].iw=ww[x]+MInt(g+h,cc)
        arr[y].iw=ww[x]+MInt(g+h,cc)



label=np.zeros([n],dtype=np.int)

img = np.zeros([height,width,3],dtype=np.uint8)
col=np.zeros([n,3],dtype=np.uint8)
# Random color values for each of the vertices
for i in range(0,n):
    label[i]=-1;
    col[i][0]=random.randint(0,255)
    col[i][1]=random.randint(0,255)
    col[i][2]=random.randint(0,255)

z=0
chippi = np.zeros([height,width],dtype=np.uint8)
for i in range(0,n):
    temp=find(i)
    if(label[temp]==-1):
        label[temp]=z
        z=z+1
    x=int(i/width)
    y=i%width
    chippi[x][y]=label[temp]


print('\nNumber of segments = ',z)

cv2.imwrite('D:/River_morpholory/Practice/label.png',chippi)

for i in range(0,n):
    y=i%width
    x=int(i/width)
    j=find(i)
    img[x][y][0]=col[j][0]
    img[x][y][1]=col[j][1]
    img[x][y][2]=col[j][2]

cv2.imwrite('D:/River_morpholory/Practice/riv.png',img)
cv2.imshow('image',img)
cv2.imshow('image1',Ii)
