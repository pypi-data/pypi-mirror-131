"Base Refined Cross-Multiscale Entropy function."
import numpy as np 
from scipy.signal import butter, filtfilt
from matplotlib.pyplot import figure, axes, show
from copy import deepcopy

def rXMSEn(Sig, Mbjx, Scales=3, F_Order=6, F_Num=.5, RadNew=0, Plotx=False):
    """rXMSEn  returns the refined multiscale cross-entropy between two   univariate data sequences.
            
    .. code-block:: python

        MSx, CI = rXMSEn(Sig, Mobj) 
        
    Returns a vector of refined multiscale cross-entropy values (``MSx``) and
    the complexity index (``CI``) between the data sequences contained in ``Sig``
    using the parameters specified by the multiscale object (``Mobj``) and the
    following default parameters:   Scales = 3, Butterworth LPF Order = 6,
    Butterworth LPF cutoff frequency at scale (T): Fc = 0.5/T. 
    If the entropy function specified by ``Mobj`` is ``XSampEn`` or ``XApEn``, ``rMSEn``
    updates the threshold radius of the data sequences (Xt) at each scale
    to 0.2*std(Xt) if no ``r`` value is provided by Mobj, or r*std(Xt) if ``r``
    is specified.
     
    .. code-block:: python
    
        MSx, CI = rXMSEn(Sig, Mobj, keyword = value, ...)
        
    Returns a vector of refined multiscale cross-entropy values (``MSx``) and 
    the complexity index (``CI``) between the data sequences contained in ``Sig``
    using the parameters specified by the multiscale object (``Mobj``) and the
    following 'keyword' arguments:
        :Scales:   - Number of temporal scales, an integer > 1 (default: 3)
        :F_Order:  - Butterworth low-pass filter order, a positive integer (default: 6)
        :F_Num:    - Numerator of Butterworth low-pass filter cutoff frequency, a scalar value in range [0 < ``F_Num`` < 1]. The cutoff frequency  at each scale (T) becomes: Fc = ``F_Num``/T.  (default: 0.5)
        :RadNew:   - Radius rescaling method, an integer in the range [1 4].
                     When the cross-entropy specified by ``Mobj`` is ``XSampEn`` or ``XApEn``, RadNew rescales the radius threshold in each sub-sequence
                     at each time scale (Ykj). If a radius value (``r``) is specified by ``Mobj``, this becomes the rescaling coefficient, otherwise
                     it is set to 0.2 (default). The value of RadNew specifies one of the following methods:
                         
                        * [1] Standard Deviation          - ``r*std(Ykj)``
                        * [2] Variance                    - ``r*var(Ykj)``
                        * [3] Mean Absolute Deviation     - ``r*mad(Ykj)``
                        * [4] Median Absolute Deviation   - ``r*mad(Ykj,1)``
                        
        :Plotx:   - When ``Plotx == True``, returns a plot of the entropy value at each time scale (i.e. the multiscale entropy curve) [default: False]
    
    :See also:
        ``MSobject``, ``XMSEn``, ``cXMSEn``, ``hXMSEn``, ``XSampEn``, ``XApEn``, ``MSEn``, ``rMSEn``
      
    :References:
        [1] Matthew W. Flood,
            "rXMSEn - EntropyHub Project"
            2021, https://github.com/MattWillFlood/EntropyHub
      
        [2] Rui Yan, Zhuo Yang, and Tao Zhang,
            "Multiscale cross entropy: a novel algorithm for analyzing two
            time series." 
            5th International Conference on Natural Computation. 
            Vol. 1, pp: 411-413 IEEE, 2009.
      
        [3] José Fernando Valencia, et al.,
            "Refined multiscale entropy: Application to 24-h holter 
            recordings of heart period variability in healthy and aortic 
            stenosis subjects." 
            IEEE Transactions on Biomedical Engineering 
            56.9 (2009): 2202-2213.
      
        [4] Puneeta Marwaha and Ramesh Kumar Sunkaria,
            "Optimal selection of threshold value ‘r’for refined multiscale
            entropy." 
            Cardiovascular engineering and technology 
            6.4 (2015): 557-576.
      
        [5] Yi Yin, Pengjian Shang, and Guochen Feng, 
            "Modified multiscale cross-sample entropy for complex time 
            series."
            Applied Mathematics and Computation 
            289 (2016): 98-110.
      
        [6] Antoine Jamin, et al,
            "A novel multiscale cross-entropy method applied to navigation 
            data acquired with a bike simulator." 
            41st annual international conference of the IEEE EMBC
            IEEE, 2019.
      
        [7] Antoine Jamin and Anne Humeau-Heurtier. 
            "(Multiscale) Cross-Entropy Methods: A Review." 
            Entropy 
            22.1 (2020): 45.
      
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
    assert isinstance(F_Order, int) and F_Order>0, \
    "F_Order:    a positive integer"
    assert isinstance(F_Num,float) and 0<F_Num<1, \
    "F_Num:     a scalar value in range [0 < F_Num < 1]"   
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
        print(' .', end='')
        Temp = refined(Sig,T,F_Order,F_Num)
        if RadNew > 0:
            Mobj.Kwargs.update({'r': Cx*Rnew(Temp)})            
        Tempx = Mobj.Func(Temp,**Mobj.Kwargs)
        if isinstance(Tempx,tuple):
            if isinstance(Tempx[0],(int,float)):
                MSx[T-1] = Tempx[0]
            else:
                MSx[T-1] =Tempx[0][-1]
        elif isinstance(Tempx,(int,float)):
                MSx[T-1] = Tempx
        elif isinstance(Tempx,np.ndarray):
                MSx[T-1] = Tempx[-1]
            
    CI = sum(MSx)
    if np.any(np.isnan(MSx)):
        print('Some entropy values may be undefined.')
    
    print('\n')

    if Plotx:       
       figure()
       ax1 = axes()   
       ax1.plot(np.arange(1,Scales+1), MSx, color=(8/255, 63/255, 77/255), linewidth=3)
       ax1.scatter(np.arange(1,Scales+1), MSx, 60, color=(1,0,1))
       ax1.set_xlabel('Scale Factor',fontsize=12,fontweight='bold',color=(7/255, 54/255, 66/255))
       ax1.set_ylabel('Entropy Value',fontsize=12,fontweight='bold',color=(7/255, 54/255, 66/255))
       ax1.set_title('Refined Multiscale %s'%(Mobj.Func.__name__), 
                     fontsize=16,fontweight='bold',color=(7/255, 54/255, 66/255))      
       show()
    
    return MSx, CI


def refined(Z,sx,P1,P2):
    bb, aa = butter(P1, P2/sx)
    Yt = filtfilt(bb, aa, Z, axis=0)
    Y = Yt[::sx,:]
    return Y   