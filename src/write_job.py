import numpy as np
import scipy





def create_job(alpha,J,name,h,m,s,path):


       with open('test_job.sh','w') as f:

            f.write('#!/bin/bash')
            f.write('\n')
 
            f.write('#SBATCH --mail-type=END,FAIL\n') 
            f.write('#SBATCH --mail-user=sxt174030@utdallas.edu\n')
            f.write('#SBATCH -J vasp_'+str(alpha)+'_'+str(J)+'_'+str(name)+'\n')          
            f.write('#SBATCH -o vasp_'+str(alpha)+'_'+str(J)+'_'+str(name)+'.out\n')
            f.write('#SBATCH -e vasp_'+str(alpha)+'_'+str(J)+'_'+str(name)+'.err\n')
            f.write('#SBATCH -n 64\n')        
            f.write('#SBATCH -N 1 \n')
            f.write('#SBATCH -p normal\n')     
            f.write('#SBATCH -t '+str(h)+':'+str(m)+':'+str(s)+'\n') 
            f.write('ibrun '+path+' > vasp.out')

