"""Base corrected Cross Conditional Entropy function."""
import numpy as np 

def XCondEn(Sig, m=2, tau=1, c=6, Logx=np.exp(1), Norm=False):
    """XCondEn  estimates the corrected cross-conditional entropy between two univariate data sequences.

    .. code-block:: python 
        
        XCond, SEw, SEz = XCondEn(Sig) 
        
    Returns the corrected cross-conditional entropy estimates (``XCond``) and the
    corresponding Shannon entropies (``m: SEw``, ``m+1: SEz``) for ``m`` = [1,2] 
    estimated for the data sequences contained in ``Sig`` using the default
    parameters:  embedding dimension = 2, time delay = 1, 
    number of symbols = 6, logarithm = natural
    ** Note: ``XCondEn`` is direction-dependent. Therefore, the order of the
    data sequences in ``Sig`` matters. If the first row/column of ``Sig`` is the
    sequence 'y', and the second row/column is the sequence 'u', then ``XCond`` is
    the amount of information carried by y(i) when the pattern u(i) is found.
  
    .. code-block:: python

        XCond, SEw, SEz = XCondEn(Sig, keyword = value, ...)
        
    Returns the corrected cross-conditional entropy estimates (``XCond``) for
    the data sequences contained in ``Sig`` using the specified 'keyword' arguments:
        :m:     - Embedding Dimension, an integer > 1        [default: 2]
        :tau:   - Time Delay, a positive integer             [default: 1]
        :c:     - Number of symbols, an integer > 1          [default: 6]
        :Logx:  - Logarithm base, a positive scalar          [default: natural]
        :Norm:  - Normalisation of XCond value, one of the following integers:
            * [False]  no normalisation                  [default]
            * [True]   normalises w.r.t cross-Shannon entropy.  
 
    :See also:
        ``XFuzzEn``, ``XSampEn``, ``XApEn``, ``XPermEn``, ``CondEn``, ``XMSEn``
    
    :References:
        [1] Alberto Porta, et al.,
            "Conditional entropy approach for the evaluation of the 
            coupling strength." 
            Biological cybernetics 
            81.2 (1999): 119-129.
         
    """
  
    Sig = np.squeeze(Sig)
    if Sig.shape[0] == 2:
        Sig = Sig.transpose()        
    N = Sig.shape[0]
    assert N>10 and min(Sig.shape)==2,  "Sig:   must be a numpy vector"
    assert isinstance(m,int) and (m > 1), "m:     must be an integer > 1"
    assert isinstance(tau,int) and (tau > 0), "tau:   must be an integer > 0"
    assert isinstance(c,int) and (c > 1), "c:   must be an integer > 1"
    assert isinstance(Logx,(int,float)) and (Logx>0), "Logx:     must be a positive value"
    assert isinstance(Norm,bool), "Norm:     must be boolean - True or False"

    S1 = (Sig[:,0]-np.mean(Sig[:,0]))/np.std(Sig[:,0])
    S2 = (Sig[:,1]-np.mean(Sig[:,1]))/np.std(Sig[:,1])   
    Edges = np.arange(min(S1),max(S1),np.ptp(S1)/c)
    Sx1 = np.digitize(S1,Edges)   
    Edges = np.arange(min(S2),max(S2),np.ptp(S2)/c)
    Sx2 = np.digitize(S2,Edges)
       
    SEw = np.zeros(m-1)
    SEz = np.zeros(m-1)
    Prcm = np.zeros(m-1)
    Xi = np.zeros((N,m))
    
    for k in range(1,m):
        Nx = N-(k-1)*tau
        Xi[:Nx,-k] = Sx1[(k-1)*tau:]        
        Wi = np.inner(c**np.arange(k-1,-1,-1),Xi[:Nx,-k:])
        Zi = (c**k)*Sx2[(k-1)*tau:] + Wi   
        Pw, _ = np.histogram(Wi,np.arange(min(Wi)-.5,max(Wi)+1.5))
        Pz, _ = np.histogram(Zi,np.arange(min(Zi)-.5,max(Zi)+1.5))
        Prcm[k-1] = sum(Pz==1)/Nx
        
        if sum(Pw)!=Nx or sum(Pz)!=Nx:
            print('Warning: Potential error estimating probabilities.')
        Pw = Pw[Pw!=0]; Pw = Pw/N
        Pz = Pz[Pz!=0]; Pz = Pz/N
        SEw[k-1] = -sum(Pw*np.log(Pw)/np.log(Logx))
        SEz[k-1] = -sum(Pz*np.log(Pz)/np.log(Logx))
        del Pw, Pz, Wi, Zi
        
    Temp, _ = np.histogram(Sx2,c)
    Temp = Temp[Temp!=0]/N
    Sy = -np.sum(Temp*np.log(Temp)/np.log(Logx))
    XCond = SEz - SEw + Prcm*Sy
    XCond = np.hstack((Sy, XCond))
    if Norm:
        XCond = XCond/Sy
    
    return XCond, SEw, SEz