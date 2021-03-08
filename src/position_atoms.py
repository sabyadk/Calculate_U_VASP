import numpy as np
import scipy 
import matplotlib.pyplot as plt
import argparse
import math
import cmath
import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")





def shuffle_ar(atom_pos,natoms,ntot):
  import random 
  N=int(natoms[-1])
  aa=[]
  print N
  for i in range(N):
    print i+int(ntot)-N 
    aa.append(i+int(ntot)-N)
  
  aa=np.array(aa)
  print np.shape(aa)
  aa=random.sample(aa,len(aa))
  atom_pos2=np.zeros((len(aa),3),dtype=float)
  for i in range(len(aa)):
     l=i+ntot-N
     print[l,aa[i]]
     
     atom_pos2[i,:]=atom_pos[aa[i],:]
    # print[atom_pos2[l,:],atom_pos[aa[i],:]]
  atom_pos[ntot-N:ntot,:]=atom_pos2[:,:]
  return atom_pos

def add_atoms(atom_pos,pos_new):

   pos_new=pos_new.astype('int')
   N=len(atom_pos[:,0])
   atom_pos2=np.zeros((N,3),dtype=float)
   for i in range(N):
    atom_pos2[i,:]=atom_pos[i,:]
   for i in range(len(pos_new)):
       
       print([i,pos_new[i],N-i-1])

       T=atom_pos[N-i-1,:]
       B=atom_pos[pos_new[i]-1,:]

 
       atom_pos2[pos_new[i]-1,:]=T
   
       atom_pos2[N-i-1,:]=B
       
#   for i in range(    
#        atom_pos[i,:]=atom_pos[i,:]


   return atom_pos2


def gen_POSCAR(lattice_vec,atom_pos,natoms,material):

      with open('POSCAR_new','w') as f:

             f.write(' system\n')
             f.write(' 1\n')
             
             f.write('   '+str(lattice_vec[0,0])+'   '+str(lattice_vec[0,1])+'   '+str(lattice_vec[0,2])+'\n')
             f.write('   '+str(lattice_vec[1,0])+'   '+str(lattice_vec[1,1])+'   '+str(lattice_vec[1,2])+'\n')
             f.write('   '+str(lattice_vec[2,0])+'   '+str(lattice_vec[2,1])+'   '+str(lattice_vec[2,2])+'\n')
             f.write('   '+material+'\n')
             f.write('   '+str(natoms)+'\n')
             f.write('   Direct\n')
        
             for i in range(len(atom_pos[:,0])):
               
               
                  
                       f.write('    '+str(atom_pos[i,0])+'    '+str(atom_pos[i,1])+'    '+str(atom_pos[i,2])+'\n')




def dist(A,B):

   d=math.sqrt((A[0]-B[0])**2+(A[1]-B[1])**2+(A[2]-B[2])**2)

   return d
def anglecalc(Bx,By,x_pos,y_pos):

              X=(Bx-x_pos)
              Y=(By-y_pos)
              

              
              if ((Y>=0)&(X<0)):
                  angle=-math.atan((-Y/X))+math.radians(180)


              elif((Y<=0)&(X<0)):
                  angle=math.atan(((-Y)/(-X)))+math.radians(180)
              elif((Y<=0)&(X>0)):
                  angle=-math.atan(-Y/X)+math.radians(360)

              else:
                  try:
                   angle=math.atan(Y/X)
                  except RuntimeWarning:
                   angle=0
              return angle

def angle(A,B):

             phi_xz=anglecalc(B[0],B[2],A[0],A[2])
             phi_xy=anglecalc(B[0],B[1],A[0],A[1])
             phi_yz=anglecalc(B[1],B[2],A[1],A[2])


             return([phi_xy,phi_xz,phi_yz])


def mat_calc(atom_pos,natoms,materials):
  near_neigh=[]
  mat=[]
  l=0
  prev=0

  for i in range(len(atom_pos[:,0])):
    B=[]
    if i>=natoms[l]+prev:
      prev=prev+natoms[l]
      l=l+1

    if(i<(natoms[l]+prev)):
      mat.append(materials[l])

  return(mat)

def N_near_neigh_calc(atom_pos,atom_pos2,lattice_vec,a,min_bond,min_bond2,control):

  N_near_neigh=[]
  N_bond=[]
  N_angle=[]
  l=0
  prev=0
  L=np.array([[0,0,0],[0,1,0],[1,0,0],[-1,0,0],[0,-1,0],[1,1,0],[1,-1,0],[-1,1,0],[-1,-1,0]
              ,[0,0,1],[0,1,1],[1,0,1],[-1,0,1],[0,-1,1],[1,1,1],[1,-1,1],[-1,1,1],[-1,-1,1]
              ,[0,0,-1],[0,1,-1],[1,0,-1],[-1,0,-1],[0,-1,-1],[1,1,-1],[1,-1,-1],[-1,1,-1],[-1,-1,-1]])
  
  for i in range(len(atom_pos2[:,0])):
    B=[]
    Bd=[]
    angle2=[]
    for m in range(len(L[:,0])):

         for j in range(len(atom_pos2[:,0])):

           blength=dist(atom_pos2[i,:],atom_pos2[j,:]+L[m,0]*lattice_vec[0,:]*a+L[m,1]*lattice_vec[1,:]*a+L[m,2]*lattice_vec[2,:]*a)
           angle3=angle(atom_pos2[i,:],atom_pos2[j,:]+L[m,0]*lattice_vec[0,:]*a+L[m,1]*lattice_vec[1,:]*a+L[m,2]*lattice_vec[2,:]*a)

           if((blength<min_bond2)&(blength>min_bond)): #&(j!=i)): last_change
    
             if j not in B:        
               
               B.append(j)
               Bd.append(blength)     
               angle2.append(angle3)       
     

    N_near_neigh.append(B)
    N_bond.append(Bd)
    N_angle.append(angle2)

  if control==1:

     return(N_near_neigh)     

  elif control==2:

     return(N_bond)   

  elif control==3:

     return(N_angle)     





def main_extract(min_bond,T=1):

  parser = argparse.ArgumentParser()
 
  parser.add_argument("--file", "-f", type=str, required=True)
  
  args = parser.parse_args()
  
  natoms2=0
  lattice_vec=np.zeros((3,3),dtype=float)
     

  with open(args.file) as f:
    j=0
    for line in f:
     
      if j==1:
        a=float(line.split()[0])
        
      elif((j>1)&(j<5)):
         lattice_vec[j-2,0]=float(line.split()[0])
         lattice_vec[j-2,1]=float(line.split()[1])
         lattice_vec[j-2,2]=float(line.split()[2])
      elif j==5:
          materials=np.array(line.split())
      elif j==6:
          natoms=np.array(line.split()).astype('int')

          for i in range(len(natoms)):
              natoms2=natoms[i]+natoms2
          atom_pos=np.zeros((natoms2,3),dtype=float)
      elif((j>7)&(j<8+natoms2)):
        atom_pos[j-8,0]=float(line.split()[0])
        atom_pos[j-8,1]=float(line.split()[1])
        atom_pos[j-8,2]=float(line.split()[2])
      
      j=j+1
  mat_typ=int(len(materials))
  atom_pos2=np.zeros((len(atom_pos[:,0]),len(atom_pos[0,:])),dtype=float)

  for j in range(len(atom_pos[:,0])):
  
 
        atom_pos2[j,:]=atom_pos[j,0]*lattice_vec[0,:]*a+atom_pos[j,1]*lattice_vec[1,:]*a+atom_pos[j,2]*lattice_vec[2,:]*a

 

  plt.show()
  mat=mat_calc(atom_pos,natoms,materials)  

  near_neigh=[]
  near_bond=[]
  near_angle=[]
  if(T==1|T==2):
    for i in range(len(min_bond)-1):

       near_neigh.append(N_near_neigh_calc(atom_pos,atom_pos2,lattice_vec,a,min_bond[i],min_bond[i+1],1))
      
       near_bond.append(N_near_neigh_calc(atom_pos,atom_pos2,lattice_vec,a,min_bond[i],min_bond[i+1],2))
     
       near_angle.append(N_near_neigh_calc(atom_pos,atom_pos2,lattice_vec,a,min_bond[i],min_bond[i+1],3))


  near_neigh=np.array(near_neigh)
  near_bond=np.array(near_bond)
#  print near_neigh[2,57]
  near_angle=np.array(near_angle)
  if T==2:

     return(atom_pos2,lattice_vec,a,near_neigh,near_angle)

  elif T==3:

     return(atom_pos2,mat,materials,natoms)

  else:
   
    return(atom_pos2,mat,near_neigh,near_bond,near_angle,materials,natoms)

def main_change():
  parser = argparse.ArgumentParser()
  #args=parser.add_argument('file', type=argparse.FileType('r'), nargs='+')
  parser.add_argument("--file", "-f", type=str, required=True)
  
  args = parser.parse_args()
  #folder='./'
  #file1='CONTCAR'
  natoms2=0
  lattice_vec=np.zeros((3,3),dtype=float)
  calc=int(input('for shuffle 1 for change_pos 2:'))
  n_chg=int(input('enter no of changes:'))
  materials=np.array(input('enter materials :')) 
  if calc==2:


#   pos_prev=np.array(input('enter change locations:'))
   pos_new=np.array(input('enter new location :'))

  with open(args.file) as f:
    j=0
    for line in f:
     
      if j==1:
        a=float(line.split()[0])
        
      elif((j>1)&(j<5)):
         lattice_vec[j-2,0]=float(line.split()[0])
         lattice_vec[j-2,1]=float(line.split()[1])
         lattice_vec[j-2,2]=float(line.split()[2])
      elif j==6:
          natoms=np.array(line.split()).astype('int')

          for i in range(len(natoms)):
              natoms2=natoms[i]+natoms2
          atom_pos=np.zeros((natoms2,3),dtype=float)
      elif((j>7)&(j<8+natoms2)):
        atom_pos[j-8,0]=float(line.split()[0])
        atom_pos[j-8,1]=float(line.split()[1])
        atom_pos[j-8,2]=float(line.split()[2])
      j=j+1
  if calc==1:

    atom_pos2=shuffle_ar(atom_pos,natoms,natoms2)
 


#   material='Se'+'   '+'W'+'   '+'Fe'
  if calc==2:
    atom_pos2=add_atoms(atom_pos,pos_new)



  material=str(materials[0])+'   '+str(materials[1])+'   '+str(materials[2])
  natoms=str(natoms[0])+'   '+str(natoms[1]-n_chg)+'   '+str(n_chg)
  gen_POSCAR(lattice_vec,atom_pos2,natoms,material)


def find_cluster_bak(atom_pos2,N_near_neigh,mat):
  from globvar import Tran_metal
  cluster=[]
  for i in range(len(atom_pos2[:,0])):

      if mat[i] in Tran_metal:

         X_NN=N_near_neigh[i]
         for j in range(len(X_NN)): 

            if mat[X_NN[j]]==mat[i]:
             if [X_NN[j],i] not in cluster: 
              cluster.append([i,X_NN[j]])
  return(cluster) 

def find_cluster(atom_pos2,N_near_neigh,mat):
  from globvar import Tran_metal
  import itertools
  cluster=[]
  for i in range(len(atom_pos2[:,0])):

      if mat[i] in Tran_metal:
         cluster2=[]
         X_NN=N_near_neigh[i]
         for j in range(len(X_NN)):

            if mat[X_NN[j]]==mat[i]:
             if [X_NN[j]] not in cluster: 
              cluster2.append(X_NN[j])
         if(len(cluster2)>0):
          
           cluster2.append(i)
           if check(cluster2,cluster)=='true':
              cluster.append(cluster2)
  return(cluster)


def check(cluster2,cluster):

   import itertools
 
   clutter=list(itertools.permutations(cluster2))
   
   for i in range(len(clutter)):

   #  print np.array(clutter[i]) 

     if np.array(clutter[i]) in np.array(cluster):

       return 'false'

   return 'true'
def cluster2(atom_pos2,N_near_neigh,mat):

     from globvar import Tran_metal
     import itertools

     cluster=[]


     for i in range(len(atom_pos2[:,0])):
             
        if mat[i] in Tran_metal:
          
          cluster2=clutter(i,N_near_neigh,mat,1)
         
          if len(cluster2)>1:
         
            if check(cluster2,cluster)=='true':
               cluster.append(cluster2)

     return cluster


def clutter(i,N_near_neigh,mat,pas):
    from globvar import Tran_metal
    t=1
    global T
    global clusterd
    if pas==1:
      T=i 
      clusterd=[]
#    print[T,i]
    if pas!=1:
#      print 'here'  
      if(i==T): 
        t=0

    if(t==0):

      return clusterd
    else:
      
      #for j in range(len(N_near_neigh[i])):
      TT=N_near_neigh[i]
#      print i
      if i not in clusterd:
              clusterd.append(i)

      for j in range(len(TT)):  
#        print(TT)
        if mat[TT[j]]==mat[i]:
           
           if TT[j] not in clusterd:     
              clusterd.append(TT[j])
              pas=pas+1  
              return(clutter(TT[j],N_near_neigh,mat,pas))

           else:
              continue
 
          
      return(clusterd)
def calc_mat(mat,typ='Trans_Metal'):


    if typ=='Trans_Metal':
      from globvar import Tran_metal
      typ1=Tran_metal

    elif typ=='Transi_Metal':
      from globvar import Transi_metal
      typ1=Transi_metal

    elif typ=='Chalcogen':
      from globvar import Chalcogen
      typ1=Chalcogen


    l=0

    for i in range(len(mat)):
      if mat[i] in typ1:
        l=l+1
    return l
        

