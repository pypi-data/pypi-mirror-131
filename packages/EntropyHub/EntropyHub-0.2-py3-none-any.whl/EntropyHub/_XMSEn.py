"Base cross-Multiscale Entropy function."
import numpy as np 
from PyEMD import EMD
from matplotlib.pyplot import figure, axes,show
from copy import deepcopy

def XMSEn(Sig, Mbjx, Scales=3, Methodx='coarse', RadNew=0, Plotx=False):
    """XMSEn  returns the multiscale cross-entropy between two univariate data sequences.
 
    .. code-block:: python
    
        MSx, CI = XMSEn(Sig, Mobj) 
        
    Returns a vector of multiscale cross-entropy values (``MSx``) and the
    complexity index (``CI``) between the data sequences contained in ``Sig`` using 
    the parameters specified by the multiscale object (``Mobj``) over 3 temporal
    scales with coarse-graining (default).
     
    .. code-block:: python
    
        MSx, CI = XMSEn(Sig, Mobj, keyword = value, ...)
        
    Returns a vector of multiscale cross-entropy values (``MSx``) and the
    complexity index (``CI``) between the data sequences contained in 'Sig' 
    using the parameters specified by the multiscale object (``Mobj``) and the
    following 'keywrod' arguments:
        :Scales:   - Number of temporal scales, an integer > 1  [default: 3]
        :Methodx:  - Graining method, one of the following: [default: ``'coarse'``]  {``'coarse'``, ``'modified'``, ``'imf'`` , ``'timeshift'``}
        :RadNew:   - Radius rescaling method, an integer in the range [1 4].
                     When the cross-entropy specified by ``Mobj`` is ``XSampEn`` or ``XApEn``, RadNew rescales the radius threshold in each sub-sequence
                     at each time scale (Ykj). If a radius value (``r``) is specified by ``Mobj``, this becomes the rescaling coefficient, otherwise
                     it is set to 0.2 (default). The value of RadNew specifies one of the following methods:
                         
                        * [1] Standard Deviation          - ``r*std(Ykj)``
                        * [2] Variance                    - ``r*var(Ykj)``
                        * [3] Mean Absolute Deviation     - ``r*mad(Ykj)``
                        * [4] Median Absolute Deviation   - ``r*mad(Ykj,1)``
                     
        :Plotx:    - When ``Plotx == True``, returns a plot of the entropy value at each time scale (i.e. the multiscale entropy curve)  [default: False]
    
    :See also:
        ``MSobject``, ``XSampEn``, ``XApEn``, ``rXMSEn``, ``cXMSEn``, ``hXMSEn``, ``MSEn``
    
    :References:
        [1] Rui Yan, Zhuo Yang, and Tao Zhang,
            "Multiscale cross entropy: a novel algorithm for analyzing two
            time series." 
            5th International Conference on Natural Computation. 
            Vol. 1, pp: 411-413 IEEE, 2009.
    
        [2] Madalena Costa, Ary Goldberger, and C-K. Peng,
            "Multiscale entropy analysis of complex physiologic time series."
            Physical review letters
            89.6 (2002): 068102.
    
        [3] Vadim V. Nikulin, and Tom Brismar,
            "Comment on “Multiscale entropy analysis of complex physiologic
            time series”." 
            Physical review letters 
            92.8 (2004): 089803.
    
        [4] Madalena Costa, Ary L. Goldberger, and C-K. Peng. 
            "Costa, Goldberger, and Peng reply." 
            Physical Review Letters
            92.8 (2004): 089804.
    
        [5] Antoine Jamin, et al,
            "A novel multiscale cross-entropy method applied to navigation 
            data acquired with a bike simulator." 
            41st annual international conference of the IEEE EMBC
            IEEE, 2019.
    
        [6] Antoine Jamin and Anne Humeau-Heurtier. 
            "(Multiscale) Cross-Entropy Methods: A Review." 
            Entropy 
            22.1 (2020): 45.
    
    """
    
    Mobj = deepcopy(Mbjx)    
    Sig = np.squeeze(Sig)  
    if Sig.shape[0] == 2:
        Sig = Sig.transpose()
    
    Chk = ['coarse','modified','imf','timeshift']    
    assert Sig.shape[0]>10 and min(Sig.shape)==2, \
    "Sig:   must be a 2-column or 2-row numpy array"    
    assert isinstance(Mobj,object) and Mobj.Func.__name__[0]=='X', "Mobj:  must \
    be a x-multiscale entropy object created with the function EntropyHub.MSobject"    
    assert isinstance(Scales,int) and Scales>1, "Scales:    must be an integer > 1"
    assert Methodx.lower() in Chk, "Methodx:  must be one of the following string names- \
    'coarse', 'modified' , 'imf', 'timeshift'"    
    assert isinstance(RadNew,int) and (np.isin(RadNew,np.arange(1,5)) \
                and Mobj.Func.__name__ in ['XSampEn','XApEn']) or RadNew==0, \
    "RadNew:     must be 0, or an integer in range [1 4] with entropy function 'XSampEn' or 'XApEn'"
    assert isinstance(Plotx, bool), "Plotx:    must be boolean - True or False"
            
    if Methodx.lower()=='imf':
        EMD().FIXE = 100
        EMD().FIXE_H = 100
        S1 = EMD().emd(Sig[:,0],max_imf=Scales-1)    
        S2 = EMD().emd(Sig[:,1],max_imf=Scales-1)   
        Sig = np.zeros((Sig.shape[0],2,Scales))
        Sig[:,0,:] = S1.transpose()
        Sig[:,1,:] = S2.transpose()   

    Func2 = globals()[Methodx.lower()]
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
        Temp = Func2(Sig,T)  
        
        if Methodx.lower() == 'timeshift':
            Tempx = np.zeros(T)
            for k in range(T):
                print(' .', end='')
                if RadNew > 0:
                    Mobj.Kwargs.update({'r': Cx*Rnew(Temp[k,:])})                                    
                Tempy = Mobj.Func(Temp[k,:,:],**Mobj.Kwargs)
                
                if isinstance(Tempy,tuple):
                    if isinstance(Tempy[0],(int,float)):
                        Tempx[k] = Tempy[0]
                    else:
                        Tempx[k] =Tempy[0][-1]
                elif isinstance(Tempy,(int,float)):
                    Tempx[k] = Tempy
                elif isinstance(Tempy,np.ndarray):
                    Tempx[k] = Tempy[-1]   
                    
            Temp2 = np.mean(Tempx)
            
        else:
            if RadNew > 0:
                    Mobj.Kwargs.update({'r': Cx*Rnew(Temp[:])})            
            Tempx = Mobj.Func(Temp,**Mobj.Kwargs)
            
            if isinstance(Tempx,tuple):
                if isinstance(Tempx[0],(int,float)):
                    Temp2 = Tempx[0]
                else:
                    Temp2 =Tempx[0][-1]
            elif isinstance(Tempx,(int,float)):
                Temp2 = Tempx
            elif isinstance(Tempx,np.ndarray):
                Temp2 = Tempx[-1]        
        MSx[T-1] = Temp2
            
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
       ax1.set_title('Cross-Multiscale %s (%s-graining method)'%(Mobj.Func.__name__,Methodx), 
                     fontsize=16,fontweight='bold',color=(7/255, 54/255, 66/255))      
       show()
    
    return MSx, CI

def coarse(Z,sx):
    Ns = len(Z)//sx
    T1 = np.mean(np.reshape(Z[:sx*Ns,0],(Ns,sx)),axis=1)
    T2 = np.mean(np.reshape(Z[:sx*Ns,1],(Ns,sx)),axis=1)
    Y = np.vstack((T1,T2)).transpose()
    return Y    

def modified(Z,sx):
    Ns = len(Z) - sx +1
    Y = np.zeros((Ns,2))
    for k in range(Ns):
        Y[k,:] = np.mean(Z[k:k+sx,:],axis=0)
    return Y 

def imf(Z,sx):
    Y = np.squeeze(np.sum(Z[:,:,:sx],axis=2))
    return Y

def timeshift(Z,sx):
    Y = np.zeros((sx,len(Z)//sx,2))
    Y[:,:,0] = np.reshape(Z[:sx*(len(Z)//sx),0],(len(Z)//sx,sx)).transpose()
    Y[:,:,1] = np.reshape(Z[:sx*(len(Z)//sx),1],(len(Z)//sx,sx)).transpose()   
    return Y