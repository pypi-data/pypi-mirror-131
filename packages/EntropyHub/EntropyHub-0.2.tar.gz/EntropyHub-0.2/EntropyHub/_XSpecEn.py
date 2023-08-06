"""Base Cross Spectral Entropy function."""
import numpy as np  

def XSpecEn(Sig, N=None, Freqs=(0,1), Logx=np.exp(1), Norm=True):
    """XSpecEn  estimates the cross-spectral entropy between two univariate data sequences.

    .. code-block:: python

        XSpec, BandEn = XSpecEn(Sig) 
        
    Returns the cross-spectral entropy estimate (``XSpec``) of the full cross-
    spectrum and the within-band entropy (``BandEn``) estimated for the data 
    sequences contained in ``Sig`` using the default  parameters: 
    N-point FFT = length of ``Sig``, normalised band edge frequencies = [0 1],
    logarithm = base 2, normalisation = w.r.t # of spectrum/band frequency 
    values.
 
    .. code-block:: python
    
        XSpec, BandEn = XSpecEn(Sig, keyword = value, ...)
        
    Returns the cross-spectral entropy (``XSpec``) and the within-band entropy 
    (``BandEn``) estimate for the data sequences contained in ``Sig`` using the
    following specified 'keyword' arguments:
        :N:     - Resolution of spectrum (N-point FFT), an integer > 1
        :Freqs: - Normalised and edge frequencies, a scalar in range [0 1]  where 1 corresponds to the Nyquist frequency (Fs/2).
              * Note: When no band frequencies are entered, ``BandEn == SpecEn``
        :Logx:  - Logarithm base, a positive scalar     [default: natural]
        :Norm:  - Normalisation of ``XSpec`` value, one of the following integers:
            [false]  no normalisation.
            [true]   normalises w.r.t # of frequency values within the spectrum/band   [default]
    
    See the `EntropyHub guide <https://github.com/MattWillFlood/EntropyHub/blob/main/EntropyHub%20Guide.pdf>`_ for more info.
 
    
    :See also:
        ``SpecEn``, ``fft``, ``XDistEn``, ``periodogram``, ``XSampEn``, ``XApEn``
     
    :References:
        [1] Matthew W. Flood,
            "XSpecEn - EntropyHub Project"
            (2021) https://github.com/MattWillFlood/EntropyHub
    
    """

    Sig = np.squeeze(Sig)
    if Sig.shape[1] == 2:
        Sig = Sig.transpose()
    if N is None:
        N = 2*Sig.shape[1] + 1
       
    assert Sig.shape[1]>10 and min(Sig.shape)==2,  "Sig:   must be a numpy vector"
    assert N>1 and isinstance(N,int), "N:   must be an integer > 1"
    assert isinstance(Logx,(int,float)) and (Logx>0), "Logx:     must be a positive value"
    assert isinstance(Norm,bool), "Norm:     must be boolean - True or False"       
    assert isinstance(Freqs,tuple) and len(Freqs)==2 and Freqs[0]>=0 and Freqs[1]<=1,\
            "Freq:    must be a two element tuple with values in range [0 1]. \
                      The values must be in increasing order."      
            
    S1 = Sig[0,:] 
    S2 = Sig[1,:]    
    Fx = int(np.ceil(N/2))
    Freqs = np.round(np.array(Freqs)*Fx).astype(int)-1
    Freqs[Freqs==-1] = 0
    
    if Freqs[0] > Freqs[1]:
        raise Exception('Lower band frequency must come first.')
    elif np.diff(Freqs) < 1:
        raise Exception('Spectrum resoution too low to determine bandwidth.')
    elif min(Freqs)<0 or max(Freqs)> Fx:
        raise Exception('Freqs must be normalized w.r.t sampling frequency [0 1].')  
        
    Pt = abs(np.fft.fft(np.convolve(S1,S2),N))
    Pxx = Pt[:Fx]/sum(Pt[:Fx])
    XSpec = -sum(Pxx*np.log(Pxx))/np.log(Logx)
    Pband = Pxx[Freqs[0]:Freqs[1]+1]/sum(Pxx[Freqs[0]:Freqs[1]+1])
    BandEn = -sum(Pband*np.log(Pband))/np.log(Logx)
    
    if Norm:
        XSpec = XSpec/(np.log(Fx)/np.log(Logx))
        BandEn = BandEn/(np.log(np.diff(Freqs)[0]+1)/np.log(Logx))
    return XSpec, BandEn