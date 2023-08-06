"""Base Cross Approximate Entropy function."""
import numpy as np    

def XApEn(Sig, m=2, tau=1, r=None, Logx=np.exp(1)):
    """XApEn  estimates the cross-approximate entropy between two univariate data sequences.

    .. code-block:: python
    
        XAp, Phi = XApEn(Sig)
        
    Returns the cross-approximate entropy estimates (``XAp``) and the average
    number of matched vectors (``Phi``) for ``m`` = [0,1,2], estimated for the data
    sequences contained in 'Sig' using the default parameters:
    embedding dimension = 2, time delay = 1, 
    radius distance threshold = 0.2*SD(Sig),  logarithm = natural
    
    **NOTE: ``XApEn`` is direction-dependent. Thus, the first row/column of ``Sig`` is used as the template data sequence, and the second row/column is the matching sequence.
 
     .. code-block:: python
       
         XAp, Phi = XApEn(Sig, keyword = value, ...)
        
    Returns the cross-approximate entropy estimates (``XAp``) between the data
    sequences contained in ``Sig`` using the specified 'keyword' arguments:
        :m:     - Embedding Dimension,  a positive integer   [default: 2]
        :tau:   - Time Delay, a positive integer        [default: 1]
        :r:     - Radius Distance Threshold, a positive scalar [default: 0.2*SD(``Sig``)]
        :Logx:  - Logarithm base, a positive scalar     [default: natural]
 
    :See also:
        ``XSampEn``, ``XFuzzEn``, ``XMSEn``, ``ApEn``, ``SampEn``, ``MSEn``
    
    :References:
        [1] Steven Pincus and Burton H. Singer,
            "Randomness and degrees of irregularity." 
            Proceedings of the National Academy of Sciences 
            93.5 (1996): 2083-2088.
    
        [2] Steven Pincus,
            "Assessing serial irregularity and its implications for health."
            Annals of the New York Academy of Sciences 
            954.1 (2001): 245-267.
    
    """
   
    Sig = np.squeeze(Sig)
    if r is None:
        r = 0.2*np.std(Sig)    
    if Sig.shape[0] == 2:
        Sig = Sig.transpose()        
    N = Sig.shape[0]
    assert N>10 and min(Sig.shape)==2,  "Sig:   must be a numpy vector"
    assert isinstance(m,int) and (m > 0), "m:     must be an integer > 0"
    assert isinstance(tau,int) and (tau > 0), "tau:   must be an integer > 0"
    assert isinstance(r,(int,float)) and (r>=0), "r:     must be a positive value"
    assert isinstance(Logx,(int,float)) and (Logx>0), "Logx:     must be a positive value"
    
    S1 = Sig[:,0]; S2 = Sig[:,1]
    Counter = 1*(abs(np.expand_dims(S2,axis=0) -np.expand_dims(S1,axis=1))<= r)  
    M = np.hstack((m*np.ones(N-m*tau), np.repeat(np.arange(m-1,0,-1),tau)))
    XAp = np.zeros((m+1))
    Phi = np.zeros((m+2))    
    for n in range(M.shape[0]):
        ix = np.where(Counter[n, :] == 1)[0]        
        for k in range(1, int(M[n]+1)):
            ix = ix[ix + (k*tau) < N]     
            if not len(ix):
                break            
            p1 = np.tile(S1[n:n+1+(tau*k):tau], (ix.shape[0], 1))                       
            p2 = S2[np.expand_dims(ix,axis=1) + np.arange(0,(k*tau)+1,tau)]           
            ix = ix[np.amax(abs(p1-p2), axis=1) <= r] 
            Counter[n, ix] += 1
            
    Phi[0] = (np.log(N)/np.log(Logx))/N
    # Phi[1] = np.mean(np.log(np.sum(Counter>0,axis=0)/N)/np.log(Logx))
    Temp = np.sum(Counter>0,axis=0); Temp = Temp[Temp!=0]
    Phi[1] = np.mean(np.log(Temp/N)/np.log(Logx))
    XAp[0]  = Phi[0] - Phi[1]
    
    for k in range(m):
        ai = np.sum(Counter>k+1,axis=0)/(N-(k+1)*tau)
        bi = np.sum(Counter>k,axis=0)/(N-(k*tau))
        ai = ai[ai>0]
        bi = bi[bi>0]
        
        with np.errstate(divide='ignore', invalid='ignore'):
            Phi[k+2] = np.sum(np.log(ai)/np.log(Logx))/(N-(k+1)*tau)
            XAp[k+1]  = np.sum(np.log(bi)/np.log(Logx))/(N-(k*tau)) - Phi[k+2]
        
    return XAp, Phi