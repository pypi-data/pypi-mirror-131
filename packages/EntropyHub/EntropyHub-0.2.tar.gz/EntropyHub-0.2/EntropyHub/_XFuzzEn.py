"""Base Cross Fuzzy Entropy function."""
import numpy as np
    
def XFuzzEn(Sig, m=2, tau=1, r=(.2,2), Fx= 'default', Logx=np.exp(1)):
    """XFuzzEn  estimates the cross-fuzzy entropy between two univariate data sequences.

    .. code-block:: python
    
        XFuzz, Ps1, Ps2 = XFuzzEn(Sig) 
    
    Returns the cross-fuzzy entropy estimates (``XFuzz``) and the average fuzzy
    distances (``m: Ps1``, ``m+1: Ps2``) for ``m`` = [1,2] estimated for the data sequences
    contained in ``Sig``, using the default parameters: embedding dimension = 2,
    time delay = 1, fuzzy function (``Fx``) = 'default', 
    fuzzy function parameters (``r``) = (0.2, 2), logarithm = natural
    
    .. code-block:: python
    
        XFuzz, Ps1, Ps2 = XFuzzEn(Sig, keyword = value, ...)
        
    Returns the cross-fuzzy entropy estimates (``XFuzz``) for dimensions = [1, ..., ``m``]
    estimated for the data sequences in 'Sig' using the specified 'keyword' arguments:
        :m:     - Embedding Dimension, a positive integer   [default: 2]
        :tau:   - Time Delay, a positive integer            [default: 1]
        :Fx:    - Fuzzy function name, one of the following strings:  {``'sigmoid'``, ``'modsampen'``, ``'default'``, ``'gudermannian'``, ``'linear'``}
        :r:     - Fuzzy function parameters, a 1 element scalar or a 2 element vector of positive values. The ``r`` parameters for each fuzzy function are defined as follows:      [default: (.2, 2)]
              
                  - sigmoid:      
                      * r(1) = divisor of the exponential argument
                      * r(2) = value subtracted from argument (pre-division)
                  - modsampen:    
                      * r(1) = divisor of the exponential argument
                      * r(2) = value subtracted from argument (pre-division)
                  - default:  
                      * r(1) = divisor of the exponential argument
                      * r(2) = argument exponent (pre-division)
                  - gudermannian:   
                      * r  = a scalar whose value is the numerator of  argument to gudermannian function: GD(x) = atan(tanh(r/x)). GD(x) is normalised to have a maximum value of 1.
                  - linear:        
                      r  = an integer value. When r = 0, the argument of the exponential function is 
                      normalised between [0 1]. When r = 1, the minimuum value of the exponential argument is set to 0.    
                                   
    :Logx:  - Logarithm base, a positive scalar  [default: natural]
    
    For further information on the keyword arguments, see the `EntropyHub guide <https://github.com/MattWillFlood/EntropyHub/blob/main/EntropyHub%20Guide.pdf>`_.
    
    :See also:
        ``FuzzEn``, ``XSampEn``, ``XApEn``, ``FuzzEn2D``, ``XMSEn``, ``MSEn``
    
    :References:
        [1] Hong-Bo Xie, et al.,
            "Cross-fuzzy entropy: A new method to test pattern synchrony of
            bivariate time series." 
            Information Sciences 
            180.9 (2010): 1715-1724.
     """
    
    Sig = np.squeeze(Sig)
    if Sig.shape[0] == 2:
        Sig = Sig.transpose()        
    N = Sig.shape[0]        
    assert N>10 and min(Sig.shape)==2,  "Sig:   must be a numpy vector"
    assert isinstance(m,int) and (m>0), "m:     must be an integer > 0"
    assert isinstance(tau,int) and (tau>0), "tau:   must be an integer > 0"
    assert isinstance(r,(int,float)) or ((r[0] >= 0) and len(r) ==2), "r:     must be 2 element tuple of positive values"    
    assert Fx.lower() in ['default','sigmoid','modsampen','gudermannian','linear'] \
            and isinstance(Fx,str), "Fx:    must be one of the following strings - \
            'default', 'sigmoid', 'modsampen', 'gudermannian', 'linear'"
    assert isinstance(Logx,(int,float)) and (Logx>0), "Logx:     must be a positive value"
    
    if isinstance(r,tuple) and Fx.lower()=='linear':
        r = 0
        print('Multiple values for r entered. Default value (0) used.') 
    elif isinstance(r,tuple) and Fx.lower()=='gudermannian':
        r = r[0];
        print('Multiple values for r entered. First value used.')      
        
    S1 = Sig[:,0]; S2 = Sig[:,1]         
    m = m+1      
    Fun = globals()[Fx.lower()]   
    Sx1 = np.zeros((N,m))
    Sx2 = np.zeros((N,m))    
    for k in range(m):
        Sx1[:N-k*tau,k] = S1[k*tau::]
        Sx2[:N-k*tau,k] = S2[k*tau::]
        
    Ps1 = np.zeros(m)
    Ps2 = np.zeros(m-1)
    Ps1[0] = 1    
    for k in range(2,m+1):        
        N1 = N - k*tau
        N2 = N - (k-1)*tau
        A = Sx1[:N2,:k] - np.transpose(np.tile(np.mean(Sx1[:N2,:k],axis=1),(k,1)))
        B = Sx2[:N2,:k] - np.transpose(np.tile(np.mean(Sx2[:N2,:k],axis=1),(k,1)))
        d2 = np.zeros((N2,N2))        
                    
        for p in range(N2):
            Mu2 = np.max(np.abs(A[p,:] - B),axis=1)
            d2[p,:] = Fun(Mu2,r)   
        
        Ps1[k-1] = np.mean(d2[:N1,:N1])
        Ps2[k-2] = np.mean(d2)
        
    with np.errstate(divide='ignore', invalid='ignore'):
        XFuzz = (np.log(Ps1[:-1]) - np.log(Ps2))/np.log(Logx)
        
    return XFuzz, Ps1, Ps2   

def sigmoid(x,r):
    assert isinstance(r,tuple), 'When Fx = "Sigmoid", r must be a two-element tuple.'
    y = 1/(1 + np.exp((x-r[1])/r[0]))
    return y  
def default(x,r):   
    assert isinstance(r,tuple), 'When Fx = "Default", r must be a two-element tuple.'
    y = np.exp(-(x**r[1])/r[0])
    return y     
def modsampen(x,r):
    assert isinstance(r,tuple), 'When Fx = "Modsampen", r must be a two-element tuple.'
    y = 1/(1 + np.exp((x-r[1])/r[0]));
    return y    
def gudermannian(x,r):
    if r <= 0:
        raise Exception('When Fx = "Gudermannian", r must be a scalar > 0.')
    y = np.arctan(np.tanh(r/x))    
    y = y/np.max(y)    
    return y    
def linear(x,r):    
    if r == 0 and x.shape[0]>1:    
        y = np.exp(-(x - min(x))/np.ptp(x))
    elif r == 1:
        y = np.exp(-(x - min(x)))
    elif r == 0 and x.shape[0]==1:   
        y = 0;
    else:
        print(r)
        raise Exception('When Fx = "Linear", r must be 0 or 1')
    return y