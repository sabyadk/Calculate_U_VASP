# This script submits the jobs created in folders with certain U values automatically 



import os
import numpy as np
alpha=[-0.1,0.05,0.1] #Value of U 
J=[0,1] # no of atoms whose U to be calculated





for i in range(len(alpha)):
  for j in range(len(J)):

        os.chdir('./'+str(alpha[i])+'/'+str(j)+'/bare')

        os.system('sbatch test_job.sh')
        os.system('pwd')
        os.chdir('../../../')
        os.chdir('./'+str(alpha[i])+'/'+str(j)+'/scf')

        os.system('sbatch test_job.sh')
        os.chdir('../../../')
        os.system('pwd')

