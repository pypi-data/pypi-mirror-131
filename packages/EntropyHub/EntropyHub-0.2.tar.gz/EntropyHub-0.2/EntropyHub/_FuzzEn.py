import numpy as np       
""" Base Fuzzy Entropy function."""

def FuzzEn(Sig,  m=2, tau=1, r=(.2,2), Fx='default', Logx=np.exp(1)):
    """FuzzEn  estimates the fuzzy entropy of a univariate data sequence.
    
    .. code-block:: python
    
        Fuzz, Ps1, Ps2 = FuzzEn(Sig) 

    Returns the fuzzy entropy estimates (``Fuzz``) and the average fuzzy distances 
    (``m``: ``Ps1``, ``m+1``: ``Ps2``) for ``m`` = [1,2] estimated from the data sequence (``Sig``)
    using the default parameters: embedding dimension = 2, time delay = 1, fuzzy function (``Fx``) = ``'default'``,
    fuzzy function parameters (``r``) = (0.2, 2),
    logarithm = natural
 
    .. code-block:: python
        
        Fuzz, Ps1, Ps2 = FuzzEn(Sig, keyword = value, ...)
        
    Returns the fuzzy entropy estimates (``Fuzz``) for dimensions = [1, ..., ``m``]
    estimated for the data sequence (``Sig``) using the specified name/value pair arguments:
        :m:     - Embedding Dimension, a positive integer    [default: 2]
        :tau:   - Time Delay, a positive integer        [default: 1]
        :Fx:    - Fuzzy function name, one of the following strings:  {``'sigmoid'``, ``'modsampen'``, ``'default'``, ``'gudermannian'``, ``'linear'``}
        :r:     - Fuzzy function parameters, a 1 element scalar or a 2 element vector of positive values. The ``r`` parameters for each fuzzy
                  function are defined as follows:      [default: (.2 2)]
              
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
        ``SampEn``, ``ApEn``, ``PermEn``, ``DispEn``, ``XFuzzEn``, ``FuzzEn2D``, ``MSEn``
    
    :References:
        [1] Weiting Chen, et al.
            "Characterization of surface EMG signal based on fuzzy entropy."
            IEEE Transactions on neural systems and rehabilitation engineering
            15.2 (2007): 266-272.
      
        [2] Hong-Bo Xie, Wei-Xing He, and Hui Liu
            "Measuring time series regularity using nonlinear
            similarity-based sample entropy."
            Physics Letters A
            372.48 (2008): 7140-7146.
        
    """   

    Sig = np.squeeze(Sig)
    N = Sig.shape[0]    
    assert N>10 and Sig.ndim == 1, "Sig:   must be a numpy vector"
    assert isinstance(m,int) and (m > 0), "m:     must be an integer > 0"
    assert isinstance(tau,int) and (tau > 0), "tau:   must be an integer > 0"
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

    m = m+1      
    Fun = globals()[Fx.lower()]   
    Sx = np.zeros((N,m))    
    for k in range(m):
        Sx[:N-k*tau,k] = Sig[k*tau::]
    
    Ps1 = np.zeros(m)
    Ps2 = np.zeros(m-1)
    Ps1[0] = .5    
    for k in range(2,m+1):        
        N1 = N - k*tau;     N2 = N - (k-1)*tau
        T2 = Sx[:N2,:k] - np.transpose(np.tile(np.mean(Sx[:N2,:k],axis=1),(k,1)))
        d2 = np.zeros((N2-1,N2-1))        
                    
        for p in range(N2-1):
            Mu2 = np.max(np.abs(np.tile(T2[p,:],(N2-p-1,1)) - T2[p+1:,:]),axis=1)
            d2[p,p:N2] = Fun(Mu2,r)   
        
        d1 = d2[:N1-1,:N1-1]
        Ps1[k-1] = np.sum(d1)/(N1*(N1-1))
        Ps2[k-2] = np.sum(d2)/(N2*(N2-1))
        
    with np.errstate(divide='ignore', invalid='ignore'):
        Fuzz = (np.log(Ps1[:-1]) - np.log(Ps2))/np.log(Logx)    
    
    return Fuzz, Ps1, Ps2  

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

"""
    Copyright 2021 Matthew W. Flood, EntropyHub
    
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
     http://www.apache.org/licenses/LICENSE-2.0
    
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
    
    For Terms of Use see https://github.com/MattWillFlood/EntropyHub
"""