import numpy as np
import scipy
from globvar import *


def gen_INCAR(ISMEAR,SIGMA,ISPIN,EDIFF,LWAVE,ICHARG,ISYM,ENCUT,LREAL,NELM,NSIM,NPAR,AMIX,BMIX,AMIX_MAG,BMIX_MAG,LORBIT,LDAU,LDAUU,LDAUJ,LDAUL,LDAUTYPE,LDAUPRINT,LMAXMIX,natoms,NSW,EDIFFG,ISIF,IBRION,name='INCAR'):

   from i_o import LSORBIT
                
   with open(name,'w') as f:
             f.write('system\n\n\n')
             f.write('ISMEAR = '+str(ISMEAR)+'\n\n\n')
             if(ISMEAR>=0):   
                  f.write('SIGMA = '+str(SIGMA)+'\n\n\n')
             f.write('EDIFF = '+str(EDIFF)+'\n\n\n')
             f.write('LWAVE = '+str(LWAVE)+'\n\n\n')
             f.write('ICHARG = '+str(ICHARG)+'\n\n\n')
             f.write('ISYM = '+str(ISYM)+'\n\n\n')
             f.write('ENCUT = '+str(ENCUT)+'\n\n\n')
             f.write('LREAL = '+str(LREAL)+'\n\n\n')
             f.write('NELM = '+str(NELM)+'\n\n\n')
             if(NPAR==0):
                 print(' ')
             elif(NPAR>0):

               f.write('NSIM = '+str(NSIM)+'\n\n\n')
               f.write('NPAR = '+str(NPAR)+'\n\n\n')
             if(ISPIN==2):

               f.write('ISPIN = '+str(ISPIN)+'\n\n\n')
               f.write('MAGMOM = '+str(sum(natoms))+'*'+str(0.0)+'\n\n\n')
             if(NSW>0):
               f.write('IBRION = '+str(IBRION)+'\n\n\n')
               f.write('ISIF = '+str(ISIF)+'\n\n\n')
               f.write('NSW = '+str(NSW)+'\n\n\n')
               f.write('EDIFFG = '+str(EDIFFG)+'\n\n\n')

                



             f.write('\n\n\n')
             if(AMIX!=-1):
                f.write('AMIX = '+str(AMIX)+'\n')
                f.write('BMIX = '+str(BMIX)+'\n')
                f.write('AMIX_MAG = '+str(AMIX_MAG)+'\n')
                f.write('BMIX_MAG = '+str(BMIX_MAG)+'\n\n\n')

             f.write('LORBIT = '+str(LORBIT)+'\n')
             if(LSORBIT==1):
                f.write('LSORBIT = .TRUE.\n\n')

             if LDAU==1:
                
               
                f.write('LDAU = .TRUE.'+'\n')
                f.write('LDAUTYPE = '+str(LDAUTYPE)+'\n') 

                f.write('LDAUL = ')
                for i in range(len(natoms)):

                   f.write(str(LDAUL[i])+' ')

                f.write('\n')
                f.write('LDAUU = ')
                for i in range(len(natoms)):

                   f.write(str(LDAUU[i])+' ')

                f.write('\n')
                f.write('LDAUJ = ')
                for i in range(len(natoms)):

                   f.write(str(LDAUJ[i])+' ')

                f.write('\n')
                
                f.write('LDAUPRINT = '+str(LDAUPRINT)+'\n')     
                f.write('LMAXMIX = '+str(LMAXMIX)+'\n')       
#   print('Written INCAR')      






             
