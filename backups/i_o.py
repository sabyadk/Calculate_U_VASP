
import numpy as np
import scipy
import argparse
import os,sys
   

with open('io.txt') as f:


    LDAUTYPE = 3
    LDAU = 1
    LMAXMIX = 4
    EDIFF = 1E-4

    alpha = [-0.5,-0.1,0.1,0.5]      
    
    ICHARG=25
    LDAUU=25
    LDAUL=25
    LDAUPRINT=2
    LDAUJ=25
    ISMEAR = 0
    SIGMA = 0.1
    ISPIN = 2
    EDIFF = 1E-4
    LWAVE = 'False'
    ISYM = -1
    ENCUT = 450
    LREAL = 'Auto'
    NELM = 100
    NSIM = 1
    NPAR = 8
    AMIX = 0.2
    BMIX = 0.00001
    AMIX_MAG = 0.8
    BMIX_MAG = 0.00001

    LORBIT = 11
    machine = 1
 
    for line in f:
      try:
       if line.split('=')[0]=='machine':

         machine=int(line.split('=')[1])




       if line.split('=')[0]=='font':

         font=int(line.split('=')[1])

       if line.split('=')[0]=='alpha':

         alpha=np.array(line.split(',')[1:-1]).astype(float)


       if line.split('=')[0]=='V.LDAU':

         LDAU=int(line.split('=')[1])

       if line.split('=')[0]=='V.LDAUTYPE':

         LDAUTYPE=int(line.split('=')[1])

       if line.split('=')[0]=='V.LDAUL':

         LDAUL=np.array(line.split(',')[1:-1]).astype(int)

       if line.split('=')[0]=='V.LDAUU':

         LDAUU=np.array(line.split(',')[1:-1]).astype(float)

       if line.split('=')[0]=='V.LDAUJ':

         LDAUJ=np.array(line.split(',')[1:-1]).astype(float)

       if line.split('=')[0]=='V.LDAUPRINT':
 
         LDAUPRINT=int(line.split('=')[1])

       if line.split('=')[0]=='V.LMAXMIX':

         LMAXMIX=int(line.split('=')[1])

       if line.split('=')[0]=='V.ICHARG':

         ICHARG=int(line.split('=')[1])

       if line.split('=')[0]=='V.ISYM':

         ISYM=int(line.split('=')[1])

       if line.split('=')[0]=='V.SIGMA':

         SIGMA=float(line.split('=')[1])

       if line.split('=')[0]=='V.ISMEAR':

         ISMEAR=int(line.split('=')[1])

       if line.split('=')[0]=='V.LWAVE':

         LWAVE=str(line.split('=')[1])

       if line.split('=')[0]=='V.ISPIN':

         ISPIN=int(line.split('=')[1])

       if line.split('=')[0]=='V.EDIFF':

         EDIFF=float(line.split('=')[1])
       if line.split('=')[0]=='V.ENCUT':

         ENCUT=int(line.split('=')[1])

       if line.split('=')[0]=='V.LREAL':

         LREAL=str(line.split('=')[1])
       if line.split('=')[0]=='V.NELM':

         NELM=int(line.split('=')[1])
       if line.split('=')[0]=='V.NSIM':

         NSIM=int(line.split('=')[1])

       if line.split('=')[0]=='V.NPAR':

         NPAR=int(line.split('=')[1])
       if line.split('=')[0]=='V.AMIX':

         AMIX=float(line.split('=')[1])
       if line.split('=')[0]=='V.BMIX':

         BMIX=float(line.split('=')[1])
       if line.split('=')[0]=='V.BMIX_MAG':

         BMIX_MAG=float(line.split('=')[1])
       if line.split('=')[0]=='V.AMIX_MAG':

         AMIX_MAG=float(line.split('=')[1])

       if line.split('=')[0]=='V.LORBIT':

         LORBIT=int(line.split('=')[1])
 

      except IndexError:
        continue












 
