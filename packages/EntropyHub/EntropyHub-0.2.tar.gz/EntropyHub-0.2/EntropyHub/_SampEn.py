import numpy as np       
""" Base Sample Entropy function."""

def SampEn(Sig, m=2, tau=1, r=None, Logx=np.exp(1)):
    """SampEn  estimates the sample entropy of a univariate data sequence.

    .. code-block:: python
    
        Samp, A, B = SampEn(Sig) 
        
    Returns the sample entropy estimates (``Samp``) and the number of matched state
    vectors (``m: B``, ``m+1: A``) for ``m`` = [0, 1, 2] estimated from the data sequence (``Sig``)
    using the default parameters: embedding dimension = 2, time delay = 1, 
    radius threshold = 0.2*SD(``Sig``), logarithm = natural
 
    .. code-block:: python
    
        Samp, A, B = SampEn(Sig, keyword = value, ...)
        
    Returns the sample entropy estimates (``Samp``) for dimensions = [0, 1, ..., ``m``]
    estimated for the data sequence (``Sig``) using the specified keyword arguments:
        :m:     - Embedding Dimension, a positive integer
        :tau:   - Time Delay, a positive integer
        :r:     - Radius Distance Threshold, a positive scalar  
        :Logx:  - Logarithm base, a positive scalar  
 
    :See also:
        ``ApEn``, ``FuzzEn``, ``PermEn``, ``CondEn``, ``XSampEn``, ``SampEn2D``, ``MSEn``
  
    :References:
        [1] Joshua S Richman and J. Randall Moorman. 
            "Physiological time-series analysis using approximate entropy
            and sample entropy." 
            American Journal of Physiology-Heart and Circulatory Physiology 
            2000
    """
   
    Sig = np.squeeze(Sig)
    N = Sig.shape[0]  
    if r is None:
        r = 0.2*np.std(Sig)
  
    assert N>10 and Sig.ndim == 1,  "Sig:   must be a numpy vector"
    assert isinstance(m,int) and (m > 0), "m:     must be an integer > 0"
    assert isinstance(tau,int) and (tau > 0), "tau:   must be an integer > 0"
    assert isinstance(r,(int,float)) and (r>=0), "r:     must be a positive value"
    assert isinstance(Logx,(int,float)) and (Logx>0), "Logx:     must be a positive value"

    Counter = (abs(np.expand_dims(Sig,axis=1)-np.expand_dims(Sig,axis=0))<= r)*np.triu(np.ones((N,N)),1)  
    M = np.hstack((m*np.ones(N-m*tau), np.repeat(np.arange(m-1,0,-1),tau)))
    A = np.zeros(m + 1)
    B = np.zeros(m + 1)
    A[0] = np.sum(Counter)
    B[0] = N*(N-1)/2
    
    for n in range(M.shape[0]):
        ix = np.where(Counter[n, :] == 1)[0]
        
        for k in range(1,int(M[n]+1)):              
            ix = ix[ix + (k*tau) < N]
            p1 = np.tile(Sig[n: n+1+(tau*k):tau], (ix.shape[0], 1))                       
            p2 = Sig[np.expand_dims(ix,axis=1) + np.arange(0,(k*tau)+1,tau)]
            ix = ix[np.amax(abs(p1 - p2), axis=1) <= r] 
            if ix.shape[0]:
                Counter[n, ix] += 1
            else:
                break
    
    for k in range(1, m+1):
        A[k] = np.sum(Counter > k)
        B[k] = np.sum(Counter[:,:-(k*tau)] >= k)
    
    with np.errstate(divide='ignore', invalid='ignore'):
        Samp = -np.log(A/B)/np.log(Logx)
    return Samp, A, B
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