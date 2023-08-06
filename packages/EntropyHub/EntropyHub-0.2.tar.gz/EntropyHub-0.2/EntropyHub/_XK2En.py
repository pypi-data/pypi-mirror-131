"""Base cross-Kolmogorov Entropy function."""
import numpy as np

def XK2En(Sig, m=2, tau=1 , r=None, Logx=np.exp(1)):
    """XK2En  estimates the cross-Kolmogorov entropy between two univariate  data sequences.

    .. code-block:: python
    
        XK2, Ci = XK2En(Sig) 
        
    Returns the cross-Kolmogorov entropy estimates (``XK2``) and the correlation
    integrals (``Ci``) for ``m`` = [1, 2] estimated between the data sequences 
    contained in ``Sig`` using the default parameters: 
    embedding dimension = 2, time delay = 1, distance threshold (``r``) = 0.2*SD(``Sig``),
    logarithm = natural
 
    .. code-block:: python
    
        XK2, Ci = XK2En(Sig, keyword = value, ...)
        
    Returns the cross-Kolmogorov entropy estimates (``XK2``) estimated between
    the data sequences contained in ``Sig`` using the specified 'keyword' arguments:
        :m:     - Embedding Dimension, a positive integer [default: 2]
        :tau:   - Time Delay, a positive integer         [default: 1]
        :r:     - Radius Distance Threshold, a positive scalar [default: 0.2*SD(``Sig``)]
        :Logx:  - Logarithm base, a positive scalar      [default: natural]
     
    :See also:
        ``XSampEn``, ``XFuzzEn``, ``XApEn``, ``K2En``, ``XMSEn``, ``XDistEn``
    
    :References:
        [1] Matthew W. Flood,
            "XK2En - EntropyHub Project"
            (2021) https://github.com/MattWillFlood/EntropyHub
    
    """
 
    Sig = np.squeeze(Sig)
    if Sig.shape[0] == 2:
        Sig = Sig.transpose()        
    if r is None:
        r = 0.2*np.std(Sig[:])
  
    N = Sig.shape[0]    
    assert N>10 and min(Sig.shape) == 2, "Sig:   must be a numpy vector"
    assert isinstance(m,int) and (m > 0), "m:     must be an integer > 0"
    assert isinstance(tau,int) and (tau > 0), "tau:   must be an integer > 0"
    assert isinstance(r,(int,float)) and r>0, "r:     must be a positive value"
    assert isinstance(Logx,(int,float)) and (Logx>0), "Logx:     must be a positive value"
               
    m = m+1
    Z1 = np.zeros((N,m))  
    Z2 = np.zeros((N,m))  
    Ci = np.zeros(m)
    for n in range(m):
        N2 = N - n*tau
        Z1[:N2,n] = Sig[n*tau:,0]
        Z2[:N2,n] = Sig[n*tau:,1]            
        Norm = np.zeros((N2,N2))             
        for k in range(N2):
            Temp = np.tile(Z1[k,:n+1],(N2,1)) - Z2[:N2,:n+1]
            Norm[k,:] = np.linalg.norm(Temp,axis=1)                      
        Ci[n] = np.mean(Norm[:] < r)
    
    with np.errstate(divide='ignore', invalid='ignore'):
        XK2 = (np.log(Ci[:-1]/Ci[1:])/np.log(Logx))/tau
    XK2[np.isinf(XK2)] = np.NaN    
    return  XK2, Ci