import numpy as np
import scipy
import os
import shutil

def first_run(machine,test):
   from i_o import LSORBIT
   if(machine=='LOCAL'):
        os.system('cp INCAR_scf0 INCAR')

        os.system('module load intel')
        if test!=1:
           os.system('module load vasp-intel')
           if(LSORBIT==1):
               os.system('mpirun -n 4 vasp_ncl')
           else:  
               os.system('mpirun -n 4 vasp_std')
   if(machine=='TACC'):
        print 'tacc'
        from i_o import path2 
        os.system('cp INCAR_scf0 INCAR')

#        os.system('module load vasp-intel')
        os.system('ibrun '+path2+' > vasp.out')


def run(alpha,j,machine,test):

   from i_o import LSORBIT 
   if(machine=='LOCAL'):
        os.system('module load intel')
        if(LSORBIT==1):
               os.system('mpirun -n 4 vasp_ncl')
        else:
               os.system('mpirun -n 4 vasp_std')


        os.chdir('./'+str(alpha)+'/'+str(j)+'/bare')
        if(test!=1):
           if(LSORBIT==1):
               os.system('mpirun -n 4 vasp_ncl')
           else:
               os.system('mpirun -n 4 vasp_std')

           os.system('rm WAVECAR')

        os.system('pwd')         
        os.chdir('../../../')
        os.system('pwd')
        os.chdir('./'+str(alpha)+'/'+str(j)+'/scf')
        if(test!=1):
           if(LSORBIT==1):
               os.system('mpirun -n 4 vasp_ncl')
           else:
               os.system('mpirun -n 4 vasp_std')
           os.system('rm WAVECAR')

        os.system('pwd')
        os.chdir('../../../')
        os.system('pwd')

   if(machine=='TACC'):           
        from i_o import h,m,s,path
        from write_job import create_job
        os.chdir('./'+str(alpha)+'/'+str(j)+'/bare')
        create_job(alpha,j,'bare',h,m,s,path)
#        os.system('sbatch test_job.sh')
        os.system('pwd')
        os.chdir('../../../')
        os.chdir('./'+str(alpha)+'/'+str(j)+'/scf')
        create_job(alpha,j,'scf',h,m,s,path) 
#        os.system('sbatch test_job.sh')
        os.chdir('../../../')
        os.system('pwd')


 

