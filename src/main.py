import numpy as np
import scipy 
import matplotlib.pyplot as plt
from read_OUTCAR import *
from write_INCAR import * 
from globvar import *
from create_folders import create_folder,create_scf0
from position_atoms import main_extract,calc_mat

def prepare_U(ntrans,natoms,mat,alpha,j):

   from i_o import LDAUTYPE
   from globvar import Tran_metal
   LDAUU=[]
   LDAUL=[]
   LDAUJ=[]
   if(LDAUTYPE==3):
     t=0
     
     for l in range(len(mat)):
       if mat[l] in Tran_metal:
        
          if t==j:
            LDAUL.append(2)
            LDAUU.append(alpha)
            LDAUJ.append(alpha)
            t=t+1
          else:
            LDAUL.append(-1)
            LDAUU.append(0.0)
            LDAUJ.append(0.0)
            t=t+1 
       else:
         LDAUL.append(-1)
         LDAUU.append(0.0)
         LDAUJ.append(0.0)
 
   return(LDAUL,LDAUJ,LDAUU) 



def main():

   from i_o import alpha,machine,LDAU,LMAXMIX,LDAUPRINT,test,fr,isim
   from run_vasp import run,first_run

   if machine==1:
     machine='LOCAL'
     
   elif machine==2:
     machine='TACC'
     NPAR=8
     NSIM=1   
   if machine=='LOCAL':
     NPAR=0
     NSIM=0

   print('You are running ur calculation on : '+str(machine)) 
  
   atom_pos2,mat,materials,natoms=main_extract(0,T=3)
   if(isim==0):
     ntrans=calc_mat(mat)
     print('Symmetries Removed')
   else:
     ntrans=calc_mat(materials)
     print('Symmetries considered')

   create_scf0(natoms,ntrans,materials,NPAR,NSIM) 
   if(fr==1):
     first_run(machine,test)

   for i in range(len(alpha)):

      for j in range(ntrans):

     
         LDAUL,LDAUJ,LDAUU=prepare_U(ntrans,natoms,materials,alpha[i],j)

         create_folder(LDAUL,LDAUJ,LDAUU,LMAXMIX,LDAUPRINT,alpha[i],j,natoms,NPAR,NSIM)

   for i in range(len(alpha)):

      for j in range(ntrans):

         print('Running calculation for [alpha atom] : '+str([alpha[i],ntrans]))

         run(alpha[i],j,machine,test)      
   
   print('Done') 


if __name__=='__main__':
   
   print('Hubbard parameter calculation code\n Developer : Sabyasachi Tiwari')
   from i_o import LSORBIT

   if(LSORBIT==1):
	   print('*****************************************\n')

	   print('V.LSORBIT tag is on')
	   print('LSORBIT : '+str(LSORBIT))
	   print('Will run vasp_ncl code\n')
	   print('*****************************************')


   main()
