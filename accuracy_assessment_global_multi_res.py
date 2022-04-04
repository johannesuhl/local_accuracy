# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 13:55:38 2022

@author: Johannes H. Uhl, University of Colorado Boulder, USA.
"""

import os,sys
import pandas as pd
import gdal
import numpy as np
import matplotlib.pyplot as plt

test_tif = './data/test.tif' # test data
ref_tif = './data/reference.tif' # reference data 
blocksizes=[1,3,5,7,9] # block sizes (in pixel) used as analytical units.

def blockmax(inarr,blocksize):        
    n = blocksize #Height of window
    m = blocksize #Width of window        
    modulo=inarr.shape[0]%blocksize
    if modulo>0:
        padby=blocksize-modulo
        inarr_pad=np.pad(inarr,((0,padby),(0,0)),mode='constant',constant_values=0)
    else:
        inarr_pad=inarr
    modulo=inarr.shape[1]%blocksize
    if modulo>0:
        padby=blocksize-modulo
        inarr_pad=np.pad(inarr_pad,((0,0),(0,padby)),mode='constant',constant_values=0)    
    k = int(inarr_pad.shape[0] / n )   #Must divide evenly
    l = int(inarr_pad.shape[1] / m )   #Must divide evenly
    inarr_pad_blockmax = inarr_pad.reshape(k,n,l,m).max(axis=(-1,-3)) #Numpy >= 1.7.1
    return inarr_pad_blockmax


outdata=[]
for blocksize in blocksizes:

    arr_10m_ref = gdal.Open(ref_tif).ReadAsArray().astype(np.int32)
    arr_10m_test = gdal.Open(test_tif).ReadAsArray().astype(np.int32)
    
    if blocksize>1:
        arr_10m_ref_res = blockmax(arr_10m_ref,blocksize)
        arr_10m_test_res = blockmax(arr_10m_test,blocksize)
    else:
        arr_10m_ref_res = arr_10m_ref
        arr_10m_test_res = arr_10m_test
                            
    currdf=pd.DataFrame()
    currdf['ref']=arr_10m_ref_res.flatten()
    currdf['test']=arr_10m_test_res.flatten()
        
    currdf=currdf[-np.logical_and(currdf.ref==0,currdf.test==0)]
    tp=len(currdf[np.logical_and(currdf.ref==1,currdf.test==1)])
    fp=len(currdf[np.logical_and(currdf.ref==0,currdf.test==1)])
    fn=len(currdf[np.logical_and(currdf.ref==1,currdf.test==0)])
    print(blocksize,tp,fp,fn)
    outdata.append([blocksize,tp,fp,fn])

outdatadf=pd.DataFrame(outdata,columns=['blocksize','tp','fp','fn'])     
outdatadf['prec']=outdatadf.tp / (outdatadf.tp+outdatadf.fp).astype(np.float) 
outdatadf['rec']=outdatadf.tp / (outdatadf.tp+outdatadf.fn).astype(np.float) 
outdatadf.to_csv('global_accmeas_multi_blocks.csv',index=False)

fig,ax=plt.subplots()
ax.plot(outdatadf.blocksize.values,outdatadf.prec.values,label='Precision')
ax.plot(outdatadf.blocksize.values,outdatadf.rec.values,label='Recall')
ax.set_ylim([0,1])
ax.set_xlabel('Block size')
plt.legend()
plt.show()