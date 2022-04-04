# -*- coding: utf-8 -*-
"""
Created on Mon May  3 15:11:48 2021

@author: Johannes H. Uhl, University of Colorado Boulder, USA
"""

import numpy as np        

def pcc(tp,tn,fp,fn):
    try:
        accmeas = (tp+tn)/float(tp+tn+fp+fn)
        if tn==0 and tp==0:
            accmeas = 0.0                            
    except:
        accmeas = np.nan
    return accmeas

def nmi(tp,tn,fp,fn):
    try:
        nmi_nom = -1*tp*np.log(tp)-fp*np.log(fp)-fn*np.log(fn)-tn*np.log(tn)+(tp+fp)*np.log(tp+fp)+(fn+tn)*np.log(fn+tn)
        nmi_denom = (tn+fp+fn+tp)*np.log((tn+fp+fn+tp))-((tp+fn)*np.log(tp+fn) + (fp+tn)*np.log(fp+tn))
        accmeas = 1-(nmi_nom/nmi_denom)                         
    except:
        accmeas = np.nan
    return accmeas        


def recall(tp,tn,fp,fn):
    try:
        accmeas = tp/float(tp+fn)
    except:
        accmeas = np.nan
    return accmeas        

def precision(tp,tn,fp,fn):
    try:
        accmeas = tp/float(tp+fp)
    except:
        accmeas = np.nan
    return accmeas        

def kappa(tp,tn,fp,fn):
    try:
        pcc=(tn+tp)/float(tn+fp+fn+tp)
        pc1=(tp+fn)/float(tn+fp+fn+tp)
        pc2=(tp+fp)/float(tn+fp+fn+tp)
        pc3=(tn+fp)/float(tn+fp+fn+tp)
        pc4=(tn+fn)/float(tn+fp+fn+tp) #fp+fn
        pc=(pc1*pc2)+(pc3*pc4)                            
        accmeas=(pcc-pc)/float(1-pc)                            
    except:
        accmeas = np.nan
    return accmeas        

def f1(tp,tn,fp,fn):
    try:
        prec = tp/float(tp+fp)
        rec = tp/float(tp+fn)                            
        accmeas=2*(prec*rec)/float(prec+rec)                           
    except:
        accmeas = np.nan 
    return accmeas        

def gmean(tp,tn,fp,fn):
    try:
        accmeas = np.sqrt((tn/float(tn+fp))*(tp/float(tp+fn)))
    except:
        accmeas = np.nan                          
    return accmeas        

def iou(tp,tn,fp,fn):
    try:
        accmeas = tp/float(tp+fp+fn) 
    except:
        accmeas = np.nan
    return accmeas        
            
def f1_adjusted(tp,tn,fp,fn):
    try:                    
        sens1 = tp/float(tp+fn)
        prec1 = tp/float(tp+fp)                    
        sens0 = tn/float(tn+fp)
        prec0 = tn/float(tn+fn)                    
        f2 = np.divide((5*sens1*prec1),((4*sens1)+prec1))
        inv_f05 = 1.25*np.divide(sens0*prec0,(0.25*sens0)+prec0)
        adj_fmeas = np.sqrt(f2*inv_f05)                    
        accmeas = adj_fmeas
    except:
        if tn==0 or tp==0 and not (fp==0 or fn==0):
            accmeas = 0.0
        elif np.nansum([tp,tn,fp,fn])==0:
            accmeas = np.nan
        else:
            accmeas = np.nan
    return accmeas        

def abs_err(tp,tn,fp,fn):
    try:
        accmeas = (tp+fp) - (tp+fn)
    except:
        accmeas = np.nan
    return accmeas        

def rel_err(tp,tn,fp,fn):
    try:
        accmeas = ((tp+fp) - (tp+fn)) / (tp+fn)
    except:
        accmeas = np.nan
    return accmeas        
        
def abs_err_log(tp,tn,fp,fn):
    try:
        abserr = (tp+fp) - (tp+fn)
        if abserr >= 1:
            abserr_transf = np.log(1+abserr)
        if abserr <= -1:    
            abserr_transf = -1*np.log(1+np.abs(abserr))
        if abserr in [-1,1]:
            abserr_transf = 0
        if abserr ==0:
            accmeas = np.nan
        accmeas = abserr_transf                            
    except:
        accmeas = np.nan
    return accmeas             

def mcc(tp,tn,fp,fn):
    try:
        accmeas=((tp*tn)-(fp*fn))/float(np.sqrt((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn)))                            
    except:
        accmeas = np.nan
    return accmeas        


#### vector based

def pcc_2(tp,tn,fp,fn):
    accmeas = (tp+tn)/(tp+tn+fp+fn).astype(np.float32)                          
    return accmeas

def nmi_2(tp,tn,fp,fn):
    nmi_nom = -1*tp*np.log(tp)-fp*np.log(fp)-fn*np.log(fn)-tn*np.log(tn)+(tp+fp)*np.log(tp+fp)+(fn+tn)*np.log(fn+tn)
    nmi_denom = (tn+fp+fn+tp)*np.log((tn+fp+fn+tp))-((tp+fn)*np.log(tp+fn) + (fp+tn)*np.log(fp+tn))
    accmeas = 1-(nmi_nom/nmi_denom)                         
    return accmeas        


def recall_2(tp,tn,fp,fn):
    accmeas = tp/(tp+fn).astype(np.float32)
    return accmeas        

def precision_2(tp,tn,fp,fn):
    accmeas = tp/(tp+fp).astype(np.float32)
    return accmeas        

def kappa_2(tp,tn,fp,fn):
    pcc=(tn+tp)/(tn+fp+fn+tp).astype(np.float32)
    pc1=(tp+fn)/(tn+fp+fn+tp).astype(np.float32)
    pc2=(tp+fp)/(tn+fp+fn+tp).astype(np.float32)
    pc3=(tn+fp)/(tn+fp+fn+tp).astype(np.float32)
    pc4=(tn+fn)/(tn+fp+fn+tp).astype(np.float32) #fp+fn
    pc=(pc1*pc2)+(pc3*pc4)                            
    accmeas=(pcc-pc)/(1-pc).astype(np.float32)                            
    return accmeas        

def f1_2(tp,tn,fp,fn):
    prec = tp/(tp+fp).astype(np.float32)
    rec = tp/(tp+fn) .astype(np.float32)                           
    accmeas=2*(prec*rec)/(prec+rec) .astype(np.float32)                          
    return accmeas        

def gmean_2(tp,tn,fp,fn):
    accmeas = np.sqrt((tn/(tn+fp).astype(np.float32))*(tp/(tp+fn).astype(np.float32)))
    return accmeas        

def iou_2(tp,tn,fp,fn):
    accmeas = tp/(tp+fp+fn).astype(np.float32) 
    return accmeas        
            
def f1_adjusted_2(tp,tn,fp,fn):
    sens1 = tp/(tp+fn).astype(np.float32)
    prec1 = tp/(tp+fp).astype(np.float32)                    
    sens0 = tn/(tn+fp).astype(np.float32)
    prec0 = tn/(tn+fn).astype(np.float32)                    
    f2 = np.divide((5*sens1*prec1),((4*sens1)+prec1))
    inv_f05 = 1.25*np.divide(sens0*prec0,(0.25*sens0)+prec0)
    adj_fmeas = np.sqrt(f2*inv_f05)                    
    accmeas = adj_fmeas
    return accmeas        

def abs_err_2(tp,tn,fp,fn):
    accmeas = (tp+fp) - (tp+fn)
    return accmeas        

def rel_err_2(tp,tn,fp,fn):
    accmeas = ((tp+fp) - (tp+fn)) / (tp+fn)
    return accmeas        
                
def mcc_2(tp,tn,fp,fn):
    upper=(tp*tn)-(fp*fn)
    lower=np.sqrt((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))
    accmeas=np.divide(upper,lower.astype(np.float32))                                                        
    return accmeas        

def abs_err_log_2(tp,tn,fp,fn):
    abserr = (tp+fp) - (tp+fn)
    abserr_transf=abserr.copy()
    abserr_transf[abserr >= 1] = np.log(1+abserr_transf[abserr >= 1])
    abserr_transf[abserr <= 1] =-1*np.log(1+abserr_transf[abserr <= 1])
    return abserr_transf