import requests
import numpy as np

def ExampleData(SigName):
    """No Docstrings here"""
    
    Chk = ["uniform","uniform2","randintegers2","randintegers",
        "henon","chirp","gaussian","gaussian2","lorenz",
        "uniform_Mat", "gaussian_Mat", "entropyhub_Mat",
        "mandelbrot_Mat","randintegers_Mat"]
    
    if SigName not in Chk:
        raise Exception("SigName must be one of the following:\n%s" %Chk)
        
    url = r"https://raw.githubusercontent.com/MattWillFlood/EntropyHub/main/ExampleData/" + SigName + ".txt"
    resp = requests.get(url)    
    
    if SigName == 'chirp':
        Temp = np.matrix([x for x in resp.text.split('\n')][2:-1])    
        X = np.squeeze(np.array(Temp).astype(float))
    
    elif SigName in ['uniform','gaussian','randintegers']:    
        Temp = np.matrix([x for x in resp.text.split('\n')][2])    
        X = np.squeeze(np.array(Temp))
    
    else: 
        Temp = ([np.matrix([y for y in x.split()])
                         for x in resp.text.split('\r\n')[2:-1]])                         
        X = np.squeeze(np.array(Temp).astype(float))
            
    return X