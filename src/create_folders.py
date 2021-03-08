import numpy as np
import scipy 
import os
import shutil




def create_folder(LDAUL,LDAUJ,LDAUU,LMAXMIX,LDAUPRINT,alpha,j,natoms,NPAR,NSIM):

   from i_o import ISMEAR,SIGMA,ISPIN,EDIFF,LWAVE,ICHARG,ISYM,ENCUT,LREAL,NELM,AMIX,BMIX,AMIX_MAG,BMIX_MAG,LORBIT,LDAU,LDAUTYPE,NSW,EDIFFG,ISIF,IBRION 
   from write_INCAR import *
   alpha=str(alpha)
   j=str(j)  
   
   if os.path.exists('./'+str(alpha)):
      print('Folder : '+str(alpha)+' exists')
   else:
      os.system('mkdir ./'+str(alpha)) 

   os.system('mkdir ./'+str(alpha)+'/'+str(j))
   os.system('mkdir ./'+str(alpha)+'/'+str(j)+'/bare')
   ICHARG=11
   
   gen_INCAR(ISMEAR,SIGMA,ISPIN,EDIFF,LWAVE,ICHARG,ISYM,ENCUT,LREAL,NELM,NSIM,NPAR,AMIX,BMIX,AMIX_MAG,BMIX_MAG,LORBIT,LDAU,LDAUU,LDAUJ,LDAUL,LDAUTYPE,LDAUPRINT,LMAXMIX,natoms,0,EDIFFG,ISIF,IBRION) 
      
   os.system('mv INCAR '+'./'+alpha+'/'+j+'/bare'+'/')
   os.system('cp POTCAR '+'./'+alpha+'/'+j+'/bare'+'/')
   os.system('cp KPOINTS '+'./'+alpha+'/'+j+'/bare'+'/')
   os.system('cp POSCAR '+'./'+alpha+'/'+j+'/bare'+'/')
   os.system('cp CHGCAR '+'./'+alpha+'/'+j+'/bare'+'/')
   os.system('cp WAVECAR '+'./'+alpha+'/'+j+'/bare'+'/')

    
   os.system('mkdir ./'+alpha+'/'+j+'/scf')
   ICHARG=0

   gen_INCAR(ISMEAR,SIGMA,ISPIN,EDIFF,LWAVE,ICHARG,ISYM,ENCUT,LREAL,NELM,NSIM,NPAR,AMIX,BMIX,AMIX_MAG,BMIX_MAG,LORBIT,LDAU,LDAUU,LDAUJ,LDAUL,LDAUTYPE,LDAUPRINT,LMAXMIX,natoms,NSW,EDIFFG,ISIF,IBRION)  
   os.system('mv INCAR '+'./'+alpha+'/'+j+'/scf'+'/')
   
   os.system('cp POTCAR '+'./'+alpha+'/'+j+'/scf'+'/')
   os.system('cp KPOINTS '+'./'+alpha+'/'+j+'/scf'+'/')   
   os.system('cp POSCAR '+'./'+alpha+'/'+j+'/scf'+'/')

def create_scf0(natoms,ntrans,mat,NPAR,NSIM):   


   from i_o import ISMEAR,SIGMA,ISPIN,EDIFF,LWAVE,ICHARG,ISYM,ENCUT,LREAL,NELM,AMIX,BMIX,AMIX_MAG,BMIX_MAG,LORBIT,LDAU,LDAUTYPE,LDAUPRINT,LMAXMIX,NSW,EDIFFG,ISIF,IBRION
   from write_INCAR import *
   from globvar import Tran_metal
   LDAUU=[]
   LDAUJ=[]
   LDAUL=[]
   for i in range(len(natoms)):
      LDAUU.append(0.0)
      LDAUJ.append(0.0)
      if mat[i] in Tran_metal:
        LDAUL.append(2)
      else:
        LDAUL.append(-1)
     

   ICHARG=0
   LWAVE = 'TRUE'
   
   gen_INCAR(ISMEAR,SIGMA,ISPIN,EDIFF,LWAVE,ICHARG,ISYM,ENCUT,LREAL,NELM,NSIM,NPAR,AMIX,BMIX,AMIX_MAG,BMIX_MAG,LORBIT,LDAU,LDAUU,LDAUJ,LDAUL,LDAUTYPE,LDAUPRINT,LMAXMIX,natoms,NSW,EDIFFG,ISIF,IBRION,name='INCAR_scf0')

