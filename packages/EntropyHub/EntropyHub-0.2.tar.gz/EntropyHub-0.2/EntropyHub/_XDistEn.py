"""Base Cross Distribution Entropy function."""
import numpy as np    
from scipy.stats import skew

def XDistEn(Sig, m=2, tau=1, Bins='Sturges', Logx=2, Norm=True):
    """XDistEn  estimates the cross-distribution entropy between two univariate data sequences.
    
    .. code-block:: python
    
        XDist, Ppi = XDistEn(Sig) 
        
    Returns the cross-distribution entropy estimate (``XDist``) and the
    corresponding distribution probabilities (``Ppi``) estimated between the data 
    sequences contained in ``Sig`` using the default parameters: 
    embedding dimension = 2, time delay = 1, binning method = ``'Sturges'``,
    logarithm = base 2, normalisation = w.r.t # of histogram bins
 
    .. code-block:: python
    
        XDist, Ppi = XDistEn(Sig, keyword = value, ...)
        
    Returns the cross-distribution entropy estimate (``XDist``) estimated between the 
    data sequences contained in 'Sig' using the specified 'keyword' = arguments:
        :m:     - Embedding Dimension, a positive integer   [default: 2]
        :tau:   - Time Delay, a positive integer            [default: 1]
        :Bins:  - Histogram bin selection method for distance distribution,
            * an integer > 1 indicating the number of bins, or one of the 
            * following strings {``'sturges'``, ``'sqrt'``, ``'rice'``, ``'doanes'``} [default: 'sturges']
        :Logx:  - Logarithm base, a positive scalar [default: 2] (enter 0 for natural log)
        :Norm:  - Normalisation of DistEn value, a boolean value:
            * [False]  no normalisation.
            * [True]   normalises w.r.t # of histogram bins [default]
    
    :See also: 
        ``XSampEn``, ``XApEn``, ``XPermEn``, ``XCondEn``, ``DistEn``, ``DistEn2D``, ``XMSEn``
    
    :References:
        [1] Yuanyuan Wang and Pengjian Shang,
            "Analysis of financial stock markets through the multiscale
            cross-distribution entropy based on the Tsallis entropy."
            Nonlinear Dynamics 
            94.2 (2018): 1361-1376.
    
    """
    
    Sig = np.squeeze(Sig)
    if Sig.shape[0] == 2:
        Sig = Sig.transpose()     
    if Logx == 0:
        Logx = np.exp(1)
    assert Sig.shape[0]>1 and min(Sig.shape)==2,  "Sig:   must be a numpy vector"
    assert isinstance(m,int) and (m>0), "m:     must be an integer > 0"
    assert isinstance(tau,int) and (tau>0), "tau:   must be an integer > 0"
    assert isinstance(Logx,(int,float)) and (Logx>0), "Logx:     must be a positive value"
    assert isinstance(Norm,bool), "Norm:     must be boolean - True or False"
    assert (isinstance(Bins,int) and Bins > 1) \
            or (Bins.lower() in ['sturges','sqrt','rice','doanes']), \
            "Bins:    an integer > 1, or can be one of the following strings - \
            'sturges', 'sqrt', 'rice', 'doanes'"    
    
    S1 = Sig[:,0]; S2 = Sig[:,1]     
    Nx = len(S1) - ((m-1)*tau)   
    Zm1 = np.zeros((Nx,m))
    Zm2 = np.zeros((Nx,m))
    for n in np.arange(m):
        Zm1[:,n] = S1[n*tau:Nx+(n*tau)]
        Zm2[:,n] = S2[n*tau:Nx+(n*tau)]
        
    DistMat = np.zeros((Nx,Nx))
    for k in range(Nx):
        DistMat[k:] = np.max(abs(np.tile(Zm1[k,:],(Nx,1))-Zm2),axis=1)
      
    Ny = Nx*Nx
    DistMat = np.reshape(DistMat,(Ny))  
    if isinstance(Bins, str):
        if Bins.lower() == 'sturges':
            Bx = np.ceil(np.log2(Ny) + 1)
        elif Bins.lower() == 'rice':
            Bx = np.ceil(2*(Ny**(1/3)))
        elif Bins.lower() == 'sqrt':
            Bx = np.ceil(np.sqrt(Ny))
        elif Bins.lower()== 'doanes':
            sigma = np.sqrt(6*(Ny-2)/((Ny+1)*(Ny+3)))
            Bx = np.ceil(1+np.log2(Ny)+np.log2(1+abs(skew(DistMat)/sigma)))
        else:
            raise Exception('Please enter a valid binning method')               
    else:
        Bx = Bins
        
    Ppi,_ = np.histogram(DistMat,int(Bx))        
    Ppi = Ppi/Ny    
    if round(sum(Ppi),6) != 1:
        print('Warning: Potential error estimating probabilities (p = ' +str(np.sum(Ppi))+ '.')
        Ppi = Ppi[Ppi!=0]
    elif any(Ppi==0):
        print('Note: '+str(sum(Ppi==0))+'/'+str(len(Ppi))+' bins were empty')
        Ppi = Ppi[Ppi!=0]
           
    XDist = -sum(Ppi*np.log(Ppi)/np.log(Logx))
    if Norm:
        XDist = XDist/(np.log(Bx)/np.log(Logx))
      
    return XDist, Ppi