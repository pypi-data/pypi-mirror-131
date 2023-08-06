"Base composite cross-Multiscale Entropy function."
import numpy as np  
from matplotlib.pyplot import figure, axes, show
from copy import deepcopy

def cXMSEn(Sig, Mbjx,  Scales=3, RadNew=0, Refined=False, Plotx=False):
    """cXMSEn  returns the composite multiscale cross-entropy between two univariate data sequences.
 
    .. code-block:: python
        
        MSx, CI = cXMSEn(Sig, Mobj) 
        
    Returns a vector of composite multiscale cross-entropy values (``MSx``) 
    between two univariate data sequences contained in ``Sig`` using the 
    parameters specified by the multiscale object (``Mobj``) using the composite 
    multiscale method (cMSE) over 3 temporal scales.
     
    .. code-block:: python
        
        MSx, CI = cXMSEn(Sig, Mobj, keyword = value, ...)
        
    Returns a vector of composite multiscale cross-entropy values (``MSx``) 
    between the data sequences contained in 'Sig' using the parameters
    specified by the multiscale object (Mobj) and the following 'keyword' arguments:
        :Scales:   - Number of temporal scales, an integer > 1   (default: 3)
        :RadNew:   - Radius rescaling method, an integer in the range [1 4].
                     When the cross-entropy specified by ``Mobj`` is ``XSampEn`` or ``XApEn``, RadNew rescales the radius threshold in each sub-sequence
                     at each time scale (Ykj). If a radius value (``r``) is specified by ``Mobj``, this becomes the rescaling coefficient, otherwise
                     it is set to 0.2 (default). The value of RadNew specifies one of the following methods:
                         
                        * [1] Standard Deviation          - ``r*std(Ykj)``
                        * [2] Variance                    - ``r*var(Ykj)``
                        * [3] Mean Absolute Deviation     - ``r*mad(Ykj)``
                        * [4] Median Absolute Deviation   - ``r*mad(Ykj,1)``
                     
        :Refined:  - Refined-composite XMSEn method. When ``Refined == True`` and the cross-entropy function specified by ``Mobj`` is ``XSampEn``,  ``cXMSEn`` returns the refined-composite multiscale entropy (rcXMSEn) [default: False]
        :Plotx:    - When ``Plotx == True``, returns a plot of the entropy value at each time scale (i.e. the multiscale entropy curve) [default: False]
    
    :See also:
        ``MSobject``, ``XMSEn``, ``rXMSEn``, ``hXMSEn``, ``XSampEn``, ``XApEn``, ``MSEn``, ``cMSEn``, ``rMSEn``
    
    :References:
        [1] Rui Yan, Zhuo Yang, and Tao Zhang,
            "Multiscale cross entropy: a novel algorithm for analyzing two
            time series." 
            5th International Conference on Natural Computation. 
            Vol. 1, pp: 411-413 IEEE, 2009.
    
        [2] Yi Yin, Pengjian Shang, and Guochen Feng, 
            "Modified multiscale cross-sample entropy for complex time 
            series."
            Applied Mathematics and Computation 
            289 (2016): 98-110.
    
        [3] Madalena Costa, Ary Goldberger, and C-K. Peng,
            "Multiscale entropy analysis of complex physiologic time series."
            Physical review letters
            89.6 (2002): 068102.
    
        [4] Antoine Jamin, et al,
            "A novel multiscale cross-entropy method applied to navigation 
            data acquired with a bike simulator." 
            41st annual international conference of the IEEE EMBC
            IEEE, 2019.
    
        [5] Antoine Jamin and Anne Humeau-Heurtier. 
            "(Multiscale) Cross-Entropy Methods: A Review." 
            Entropy 
            22.1 (2020): 45.
    
        [6] Shuen-De Wu, et al.,
            "Time series analysis using composite multiscale entropy." 
            Entropy 
            15.3 (2013): 1069-1084.
    
    """
    
    Mobj = deepcopy(Mbjx)
    Sig = np.squeeze(Sig)  
    if Sig.shape[0] == 2:
        Sig = Sig.transpose()
    
    assert Sig.shape[0]>10 and min(Sig.shape)==2, \
    "Sig:   must be a 2-column or 2-row numpy array"    
    assert isinstance(Mobj,object) and Mobj.Func.__name__[0]=='X', "Mobj:  must \
    be a x-multiscale entropy object created with the function EntropyHub.MSobject"    
    assert isinstance(Scales,int) and Scales>1, "Scales:    must be an integer > 1"
    assert isinstance(Refined, bool) and ((Refined==True and Mobj.Func.__name__=='XSampEn')
        or Refined==False), \
    "Refined:       must be a 0 or 1. If Refined==True, Mobj.Func must be SampEn"
    assert (np.isin(RadNew,np.arange(1,5)) and Mobj.Func.__name__ in \
    ['XSampEn','XApEn']) or RadNew==0, "RadNew:     must be an integer in range \
    [1 4] and entropy function must be 'XSampEn' or 'XApEn'"
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
                Mobj.Kwargs.update({'r': Cx*Rnew(Temp[k:N:T,:])})    
                
            if Refined:
                _, Ma, Mb = Mobj.Func(Temp[k:N:T,:],**Mobj.Kwargs)
                Temp2[k] = Ma[-1]
                Temp3[k] = Mb[-1]
            else:
                Temp2 = Mobj.Func(Temp[k:N:T,:],**Mobj.Kwargs)
                
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
    
    print('\n')
            
    if Plotx == 1:
        if Refined:
            strx = 'Refined-Composite Cross-'
        else:
            strx = 'Composite Cross-'
        
        figure()
        ax1 = axes()   
        ax1.plot(np.arange(1,Scales+1), MSx, color=(8/255, 63/255, 77/255), linewidth=3)
        ax1.scatter(np.arange(1,Scales+1), MSx, 60, color=(1,0,1))
        ax1.set_xlabel('Scale Factor',fontsize=12,fontweight='bold',color=(7/255, 54/255, 66/255))
        ax1.set_ylabel('Entropy Value',fontsize=12,fontweight='bold',color=(7/255, 54/255, 66/255))
        ax1.set_title('%sMultiscale %s'%(strx,Mobj.Func.__name__), 
                     fontsize=16,fontweight='bold',color=(7/255, 54/255, 66/255))       
        show()

    return MSx, CI


def modified(Z,sx):
   Ns = Z.shape[0] - sx +1
   Y = np.zeros((Ns,2))
   for k in range(Ns):
       Y[k,:] = np.mean(Z[k:k+sx,:],axis=0)
   return Y 