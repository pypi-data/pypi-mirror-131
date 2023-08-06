"Base composite Multiscale Entropy function."
import numpy as np 
from matplotlib.pyplot import figure, axes, show
from copy import deepcopy

def cMSEn(Sig, Mbjx, Scales=3, RadNew=0, Refined=False, Plotx=False):
    """cMSEn  Returns the composite multiscale entropy of a univariate data sequence.

    .. code-block:: python 
        
        MSx, CI = cMSEn(Sig, Mobj) 
        
    Returns a vector of composite multiscale entropy values (``MSx``) for the data 
    sequence (``Sig``) using the parameters specified by the multiscale object 
    (``Mobj``) using the composite multiscale entropy method (cMSE) over 3 temporal
    scales.
     
    .. code-block:: python
        
        MSx, CI = cMSEn(Sig, Mobj, keyword = value, ...)
        
    Returns a vector of composite multiscale entropy values (``MSx``) of the 
    data sequence (``Sig``) using the parameters specified by the multiscale 
    object (``Mobj``) and the following 'keyword' arguments:
        :Scales:   - Number of temporal scales, an integer > 1   (default: 3)
        :RadNew:   - Radius rescaling method, an integer in the range [1 4].
                     When the entropy specified by ``Mobj`` is ``SampEn`` or ``ApEn``, RadNew rescales the radius threshold in each sub-sequence
                     at each time scale (Ykj). If a radius value (``r``) is specified by ``Mobj``, this becomes the rescaling coefficient, otherwise
                     it is set to 0.2 (default). The value of RadNew specifies one of the following methods:
                         
                        * [1] Standard Deviation          - ``r*std(Ykj)``
                        * [2] Variance                    - ``r*var(Ykj)``
                        * [3] Mean Absolute Deviation     - ``r*mad(Ykj)``
                        * [4] Median Absolute Deviation   - ``r*mad(Ykj,1)``
                     
        :Refined:  - Refined-composite MSEn method. When ``Refined == True`` and the entropy function specified by ``Mobj`` is ``SampEn``, 
                     ``cMSEn`` returns the refined-composite multiscale entropy (rcMSEn) [default: False]
        :Plotx:    - When Plotx == True, returns a plot of the entropy value at each time scale (i.e. the multiscale entropy curve) [default: False]
    
    :See also:
        ``MSobject``, ``MSEn``, ``rMSEn``, ``hMSEn``, ``XMSEn``, ``cXMSEn``, ``SampEn``, ``ApEn`` 
     
    :References:
        [1] Madalena Costa, Ary Goldberger, and C-K. Peng,
            "Multiscale entropy analysis of complex physiologic time series."
            Physical review letters
            89.6 (2002): 068102.
            
        [2] Vadim V. Nikulin, and Tom Brismar,
            "Comment on “Multiscale entropy analysis of complex physiologic
            time series”." 
            Physical review letters 
            92.8 (2004): 089803.
    
        [3] Madalena Costa, Ary L. Goldberger, and C-K. Peng. 
            "Costa, Goldberger, and Peng reply." 
            Physical Review Letters
            92.8 (2004): 089804.
    
        [4] Shuen-De Wu, et al.,
            "Time series analysis using composite multiscale entropy." 
            Entropy 
            15.3 (2013): 1069-1084.
    
        [5] Shuen-De Wu, et al.,
            "Analysis of complex time series using refined composite 
            multiscale entropy." 
            Physics Letters A 
            378.20 (2014): 1369-1374.
    
    """
  
    Mobj = deepcopy(Mbjx)    
    Sig = np.squeeze(Sig)    
    assert Sig.shape[0]>10 and Sig.ndim == 1, "Sig:   must be a numpy vector"    
    assert isinstance(Mobj,object), "Mobj:  must be a multiscale entropy \
    object created with the function EntropyHub.MSobject"    
    assert isinstance(Scales,int) and Scales>1, "Scales:    must be an integer > 1"
    assert isinstance(RadNew,int) and (np.isin(RadNew,np.arange(1,5)) \
                and Mobj.Func.__name__ in ['SampEn','ApEn']) or RadNew==0, \
    "RadNew:     must be 0, or an integer in range [1 4] with entropy function 'SampEn' or 'ApEn'"
    assert isinstance(Refined, bool) and ((Refined==True and Mobj.Func.__name__=='SampEn')
        or Refined==False), \
    "Refined:       must be a 0 or 1. If Refined==True, Mobj.Func must be SampEn"
    assert isinstance(Plotx, bool), "Plotx:    must be boolean - True or False"
    
    MSx = np.zeros(Scales)    
    if RadNew > 0:
        if RadNew == 1:
            Rnew = lambda x: np.std(x)
        elif RadNew == 2:
            Rnew = lambda x: np.var(x)
        elif RadNew == 3:
            Rnew = lambda x: np.mean(abs(x-np.mean(x)))
        elif RadNew == 4:
            Rnew = lambda x: np.median(abs(x-np.median(x)))    
        
        try:
            Cx = Mobj.Kwargs.get('r')*1
        except:
            Cy = ['Standard Deviation','Variance','Mean Abs Deviation',
                  'Median Abs Deviation']
            print('WARNING: No radius value provided.\nDefault set to ' \
                  '0.2*(%s) of each new time-series.'%Cy[RadNew-1])            
            Cx = .2

    for T in range(1,Scales+1):
        Temp = modified(Sig,T)    
        N = T*(len(Temp)//T)
        Temp3 = np.zeros(T)
        Temp2 = np.zeros(T)                
        for k in range(T):        
            print(' .', end='')

            if RadNew > 0:
                Mobj.Kwargs.update({'r': Cx*Rnew(Temp[k::T])})             
            if Refined:
                _, Ma, Mb = Mobj.Func(Temp[k:N:T],**Mobj.Kwargs)
                Temp2[k] = Ma[-1]
                Temp3[k] = Mb[-1]
            else:
                Temp2 = Mobj.Func(Temp[k:N:T],**Mobj.Kwargs)
                if isinstance(Temp2,tuple):
                    if isinstance(Temp2[0],(int,float)):
                        Temp3[k] = Temp2[0]
                    else:
                        Temp3[k] = Temp2[0][-1]       
                elif isinstance(Temp2,(int,float)):
                    Temp3[k] = Temp2
                elif isinstance(Temp2,np.ndarray):
                    Temp3[k] = Temp2[-1]
                     
        if Refined:
            MSx[T-1] = -np.log(sum(Temp2)/sum(Temp3))
        else:
            MSx[T-1] = np.mean(Temp3)
    
    CI = sum(MSx)
    if np.any(np.isnan(MSx)):
        print('Some entropy values may be undefined.')

    if Plotx:
        if Refined:
            strx = 'Refined-Composite'
        else:
            strx = 'Composite'
        
        figure()
        ax1 = axes()   
        ax1.plot(np.arange(1,Scales+1), MSx, color=(8/255, 63/255, 77/255), linewidth=3)
        ax1.scatter(np.arange(1,Scales+1), MSx, 60, color=(1,0,1))
        ax1.set_xlabel('Scale Factor',fontsize=12,fontweight='bold',color=(7/255, 54/255, 66/255))
        ax1.set_ylabel('Entropy Value',fontsize=12,fontweight='bold',color=(7/255, 54/255, 66/255))
        ax1.set_title('%s Multiscale %s'%(strx,Mobj.Func.__name__), 
                     fontsize=16,fontweight='bold',color=(7/255, 54/255, 66/255))       
        show()
    
    return MSx, CI


def modified(Z,sx):
    Ns = len(Z) - sx +1
    Y = np.zeros(Ns)
    for k in range(Ns):
        Y[k] = np.mean(Z[k:k+sx])
    return Y 