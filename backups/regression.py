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
from matplotlib import rc

rc('text',usetex=True)
rc('font',family='serif')


def LS(x,n,alpha):


   b=0

   T=0
   for i in range(len(alpha)):


     T=((x[0]*alpha[i]+x[1])-n[i])**2+T

   b=np.sqrt(T)
   return(b)




def regress(alpha,mat,font):
 
    from globvar import Tran_metal
    N=0
    for i in range(len(mat)):

      if mat[i] in Tran_metal:
    
         N=N+1
    print('U Matrix size :'+'['+str(N)+'X'+str(N)+']') 

    n_bare=np.zeros((len(alpha),N,N),dtype=float)
    n_scf=np.zeros((len(alpha),N,N),dtype=float)
    X_0=np.zeros((N,N),dtype=float)
    X_1=np.zeros((N,N),dtype=float)

    for i in range(len(alpha)):

      for j in range(N):
        
        n_bare[i,j,:]=np.array(charge_read('./'+str(-1*alpha[i])+'/'+str(j)+'/bare/OUTCAR',len(mat),2))[len(mat)-N:len(mat)] 
        n_scf[i,j,:]=np.array(charge_read('./'+str(-1*alpha[i])+'/'+str(j)+'/scf/OUTCAR',len(mat),2))[len(mat)-N:len(mat)]
        print(np.array(charge_read('./'+str(-1*alpha[i])+'/'+str(j)+'/scf/OUTCAR',len(mat),2))[len(mat)-N:len(mat)])      
        print(['./'+str(-1*alpha[i])+'/'+str(j)+'/bare/OUTCAR',n_bare[i,j,:]])
        print(['./'+str(-1*alpha[i])+'/'+str(j)+'/scf/OUTCAR',n_scf[i,j,:]])
    #figure=plt.figure()
    a_scf1=np.zeros((N,N),dtype=float)
    b_scf1=np.zeros((N,N),dtype=float)
    a_bare1=np.zeros((N,N),dtype=float)
    b_bare1=np.zeros((N,N),dtype=float)

    for i in range(N):
        
      for j in range(N):
         x0=[]  
         x0.append((n_bare[1,i,j]-n_bare[0,i,j])/(alpha[1]-alpha[0]))
         
         x0.append(0)
         J1=basinhopping(LS,x0,minimizer_kwargs={"args":(n_bare[:,i,j],alpha)})#,niter=b_niter,niter_success=b_success)
         print('Bare min : '+str(J1.fun))
         print(J1.x[0])
         X_0[i,j]=J1.x[0]
         a_bare=J1.x[0]
         b_bare=J1.x[1]
         a_bare1[i,j]=a_bare
         b_bare1[i,j]=b_bare
         x0=[]

         x0.append((n_scf[1,i,j]-n_scf[0,i,j])/(alpha[1]-alpha[0]))
         x0.append(0) 

         J1=basinhopping(LS,x0,minimizer_kwargs={"args":(n_scf[:,i,j],alpha)})#,niter=b_niter,niter_success=b_success)
         print('Scf min : '+str(J1.fun))
         X_1[i,j]=J1.x[0]
         a_scf=J1.x[0]
         b_scf=J1.x[1]
         a_scf1[i,j]=a_scf
         b_scf1[i,j]=b_scf
         Y=[]
         T=[]
         for tt in range(len(alpha)):
           Y.append(a_scf*alpha[tt]+b_scf)
           T.append(a_bare*alpha[tt]+b_bare)
    try:
        U=np.linalg.inv(X_0)-np.linalg.inv(X_1)

    except np.linalg.linalg.LinAlgError:
        U=np.zeros((N,N),dtype=float)

        for i in range(N):
           for j in range(N):
               if((X_1[i,j]!=0)|(X_0[i,j]!=0)):
                 U[i,j]=(1/X_0[i,j])-(1/X_1[i,j])
 

    return(n_bare,n_scf,alpha,X_0,X_1,U,a_scf1,b_scf1,a_bare1,b_bare1,N)

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
     parser.add_argument("--font", "-font",type=int,   required=False)
     parser.add_argument("--diag", "-diag",type=int,   required=False)
     
     parser.add_argument('--materials', nargs='*')
     parser.add_argument('--alpha', type=float, nargs='*')
     args = parser.parse_args()
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
      
     n_bare,n_scf,alpha,X_0,X_1,U,a_scf,b_scf,a_bare,b_bare,N=regress(alpha,materials,args.font) 
#     figure=plt.figure()
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
     
     for i in range(N):
      for j in range(N):
         T=[]
         Y=[] 
         for tt in range(len(alpha)):

            Y.append(a_scf[i,j]*alpha[tt]+b_scf[i,j])
            T.append(a_bare[i,j]*alpha[tt]+b_bare[i,j])
         if(diag==1):
            if(i==j):      
                l1,= plt.plot(alpha,n_bare[:,i,j],color='r',marker='o',linestyle='--',markersize=12)
                l2,= plt.plot(alpha,n_scf[:,i,j],color='b',marker='o',linestyle='--',markersize=12)
                l3,= plt.plot(alpha,Y,color='b')
                l4,= plt.plot(alpha,T,color='r')
         else:
                l1,= plt.plot(alpha,n_bare[:,i,j],color='r',marker='o',linestyle='--',markersize=12)
                l2,= plt.plot(alpha,n_scf[:,i,j],color='b',marker='o',linestyle='--',markersize=12)
                l3,= plt.plot(alpha,Y,color='b')
                l4,= plt.plot(alpha,T,color='r')
     plt.legend([l1,l2,l3,l4],['bare_response','SCF_response','$scf_fit$','$bare_fit$'],fontsize=font) 
     plt.axis('tight')
     plt.xlabel('$\\alpha$ (eV)',fontsize=font)
     plt.ylabel('$n$ (a.u)',fontsize=font)
     plt.xticks(fontsize=font)
     plt.yticks(fontsize=font)
     plt.savefig('U_line.pdf',format='pdf',dpi=300)
     plt.show()
     plt.close()
     print(a_scf)








    

