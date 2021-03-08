
import numpy as np
import scipy
from scipy.optimize import rosen, differential_evolution, basinhopping
import matplotlib.pyplot as plt
from read_OUTCAR import *

#plt.switch_backend('agg')
import matplotlib as mpl
mpl.rcParams['axes.linewidth'] = 1.5
#print E
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})


def LS(x,n,alpha):


   b=0

   T=0
   for i in range(len(alpha)):


     T=((x[0]*alpha[i]**2+x[1]*alpha[i]+x[2])-n[i])**2+T

   b=np.sqrt(T)
   return(b)




def LS2(x,n,alpha):


   b=0

   T=0
   for i in range(len(alpha)):


     T=((x[0]*alpha[i]+x[1])-n[i])**2+T

   b=np.sqrt(T)
   return(b)




def regress(U,alpha,mat,font):
 
    from globvar import Tran_metal
    N=0
    for i in range(len(mat)):

      if mat[i] in Tran_metal:
    
         N=N+1
    print('U Matrix size :'+'['+str(N)+'X'+str(N)+']') 

    n_scf=np.zeros((len(alpha),N,N),dtype=float)
    X_0=np.zeros((N,N),dtype=float)
    X_1=np.zeros((N,N),dtype=float)

    for i in range(len(alpha)):

      for j in range(N):
        
        n_scf[i,j,:]=np.array(charge_read('./'+str(alpha[i]),len(mat),2))[len(mat)-N:len(mat)]
        print(np.array(charge_read('./'+str(alpha[i]),len(mat),2))[len(mat)-N:len(mat)])      
        print(['./'+str(alpha[i]),n_scf[i,j,:]])
    #figure=plt.figure()
    a_scf1=np.zeros((N,N),dtype=float)
    b_scf1=np.zeros((N,N),dtype=float)
    c_scf1=np.zeros((N,N),dtype=float)

    

    for i in range(N):
        
      for j in range(N):
         x0=[]

         x0.append((n_scf[1,i,j]-n_scf[0,i,j])/(U[1]-U[0]))
         x0.append(0) 
         x0.append(0)
         J1=basinhopping(LS,x0,minimizer_kwargs={"args":(n_scf[:,i,j],U)})#,niter=b_niter,niter_success=b_success)
         print('Scf min : '+str(J1.fun))
         X_1[i,j]=J1.x[0]
         a_scf=J1.x[0]
         b_scf=J1.x[1]
         c_scf=J1.x[2]
         a_scf1[i,j]=a_scf
         b_scf1[i,j]=b_scf
         c_scf1[i,j]=c_scf
         Y=[]
         T=[]
         for tt in range(len(alpha)):
           Y.append(a_scf*U[tt]**2+b_scf*U[tt]+c_scf)
       
#    U=np.linalg.inv(X_0)-np.linalg.inv(X_1)

    

    return(n_scf,alpha,X_1,a_scf1,b_scf1,c_scf1,N)

if __name__=='__main__':
     """arguments are (num --materials --alpha) 
      type(num)-- array
      type(materials) --array
      type(alpha) --array
      additional headers --font for font of figure
                         --diag for only diagonal elements 
      where num is total number of atom for a particular material
      32 12 4 --materials Se W Mn --alpha -0.1 0.1"""
     import argparse
     parser = argparse.ArgumentParser()
     diag=0
     font=12
     parser.add_argument('num', type=int, nargs='+')
     parser.add_argument("--U", "-U",type=float, nargs='*',  required=True)

     parser.add_argument("--font", "-font",type=int,   required=False)
     parser.add_argument("--diag", "-diag",type=int,   required=False)
     
     parser.add_argument('--materials', nargs='*')
     parser.add_argument('--alpha', type=str, nargs='+')
     args = parser.parse_args()
     U=args.U  
     if(args.diag!=None):
       diag=args.diag
     if(args.font!=None):
       font=args.font
     natoms=args.num
     mat=args.materials
     alpha=args.alpha
     materials=[]
     for i in range(len(natoms)):
        for j in range(natoms[i]):
          
           materials.append(mat[i])
      
     n_scf,alpha,X_1,a_scf,b_scf,c_scf,N=regress(U,alpha,materials,args.font) 
     figure=plt.figure()
     
     for i in range(N):
      for j in range(N):
         T=[]
         Y=[] 
         for tt in range(len(alpha)):

            Y.append(a_scf[i,i]*U[tt]**2+b_scf[i,j]*U[tt]+c_scf[i,j])
           
         if(diag==1):
            if(i==j):      
                l2,= plt.plot(U,n_scf[:,i,j],color='b',marker='o',linestyle='--',markersize=12)
            #    l3,= plt.plot(U,Y,color='b')
         else:
                l2,= plt.plot(U,n_scf[:,i,j],color='b',marker='o',linestyle='--',markersize=12)
             #   l3,= plt.plot(U,Y,color='b')

     plt.legend([l2],['scf_DFT'],fontsize=font) 
     plt.axis('tight')
     plt.xlabel('$\\alpha$ (eV)',fontsize=font)
     plt.ylabel('$\\rm n$',fontsize=font)
     plt.xticks(fontsize=font)
     plt.yticks(fontsize=font)
     plt.savefig('U_line.pdf',format='pdf',dpi=300)
     plt.show()
     plt.close()
     print(a_scf)
     UU=[]
     if(diag==1):
       for i in range(len(X_1[:,0])):
          for j in range(len(X_1[0,:])):
             if(i==j):

                UU.append((1/X_0[i,j])-(1/X_1[i,j]))
       U1=np.diag(np.array(UU))
       print('U_{eff} (U-J) : '+str(UU)+' eV')
       print(' chi_{1}  : '+str(np.linalg.inv(X_1))+' eV')
       print(' chi_{0}  : '+str(np.linalg.inv(X_0))+' eV')
     else:   
       print(' U_{eff} (U-J) : '+str(U)+' eV')
       print(' chi_{1}  : '+str(np.linalg.inv(X_1))+' eV')
       print(' chi_{0}  : '+str(np.linalg.inv(X_0))+' eV')
       U1=np.diag(np.array(U))
     chi_1=np.diag(np.linalg.inv(X_1))
     chi_0=np.diag(np.linalg.inv(X_0))
     
     np.savetxt('U_eff.txt',U1)
     np.savetxt('U.txt',chi_1)
     np.savetxt('J.txt',chi_0)








    

