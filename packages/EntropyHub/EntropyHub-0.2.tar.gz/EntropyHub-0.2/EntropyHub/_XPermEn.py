"""Base Cross Permutation Entropy function."""
import numpy as np

def XPermEn(Sig, m=3, tau=1, Logx=np.exp(1)):
    """XPermEn  estimates the cross-permutation entropy between two univariate data sequences.

    .. code-block:: python
    
        XPerm = XPermEn(Sig) 
        
    Returns the cross-permuation entropy estimates (``XPerm``) estimated betweeen
    the data sequences contained in ``Sig`` using the default parameters:
    embedding dimension = 3, time delay = 1, logarithm = base 2, 
    
    .. code-block:: python
 
        XPerm = XPermEn(Sig, keyword = value, ...)
        
    Returns the permutation entropy estimates (``Perm``) estimated between the data
    sequences contained in ``Sig`` using the specified 'keyword' arguments:
        :m:     - Embedding Dimension, an integer > 2   [default: 3]
            **Note: ``XPerm`` is undefined for embedding dimensions < 3.
        :tau:   - Time Delay, a positive integer        [default: 1]
        :Logx:  - Logarithm base, a positive scalar     [default: 2]   (enter 0 for natural log). 
 
    :See also:
        ``PermEn``, ``XApEn``, ``XSampEn``, ``XFuzzEn``, ``XMSEn``
  
    :References:
        [1] Wenbin Shi, Pengjian Shang, and Aijing Lin,
            "The coupling analysis of stock market indices based on 
            cross-permutation entropy."
            Nonlinear Dynamics
            79.4 (2015): 2439-2447.
     
   """

    Sig = np.squeeze(Sig)
    if Sig.shape[0] == 2:
        Sig = Sig.transpose()    
    assert Sig.shape[0]>1 and min(Sig.shape)==2,  "Sig:   must be a numpy vector"
    assert isinstance(m,int) and (m > 2), "m:     must be an integer > 2"
    assert isinstance(tau,int) and (tau > 0), "tau:   must be an integer > 0"
    assert isinstance(Logx,(int,float)) and (Logx>0), "Logx:     must be a positive value"
            
    S1 = Sig[:,0]
    S2 = Sig[:,1]
    N = len(S1)-(m-1)*tau
    Sx1 = np.zeros((N,m))
    Sx2 = np.zeros((N,m))    
    for k in range(m):
        Sx1[:,k] = S1[k*tau:N+k*tau]
        Sx2[:,k] = S2[k*tau:N+k*tau]        
    
    Temp = np.argsort(Sx1,axis=1)
    Gx = np.zeros((N,m))
    for k in range(N):
        Gx[k,:] = Sx2[k,Temp[k,:]]
        
    Kt = np.zeros((m-2,m-2,N))
    for k in range(m-2):
        for j in range(k+1,m-1):
            G1 = Gx[:,j+1] - Gx[:,k]
            G2 = Gx[:,k] - Gx[:,j]
            Kt[k,j-1,:] = (G1*G2 > 0)
     
    Di = np.squeeze(np.sum(np.sum(Kt,1),0))
    Ppi,_ = np.histogram(Di,np.arange(-.5,((m-2)*(m-1)+2)/2))
    Ppi = Ppi[Ppi!=0]/N
    XPerm = -sum(Ppi*(np.log(Ppi)/np.log(Logx)))
    
    if round(sum(Ppi),6)!=1:
        print('Warning: Potential error with probability calculation')
        
    return XPerm