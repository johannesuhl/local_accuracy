# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 14:47:43 2022

@author: Johannes H. Uhl, University of Colorado Boulder, USA.
"""

import os,sys
import pandas as pd
import gdal
import numpy as np
import matplotlib.pyplot as plt

test_tif = './data/test.tif'
ref_tif = './data/reference.tif'   
geog_scales=[400,600,800] # spatial support in m
blocksizes=[1,3,5] # block size in px. For a block size of 3 or larger, positive instances in any cell within the block are considered true positives.
orig_res = 40 # in m or linear unit of the raster data CRS
stride=2 ### as measured in 0.5 times the geog_scale.
### e.g. stride=2 means we shift a window of geog_scale=1000 by 500m in x,y.
extract=True # perform extraction 
vis=True # focal precision recall scatterplots.

def blockmax(inarr,blocksize):        
    n = blocksize                   #Height of window
    m = blocksize                   #Width of window        
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
    inarr_pad_blockmax = inarr_pad.reshape(k,n,l,m).max(axis=(-1,-3))#Numpy >= 1.7.1
    return inarr_pad_blockmax

if extract:
    allfocaldata=[]
    for geog_scale in geog_scales:
        for blocksize in blocksizes:        

            arr_10m_ref = gdal.Open(ref_tif).ReadAsArray().astype(np.int32)
            arr_10m_test = gdal.Open(test_tif).ReadAsArray().astype(np.int32)
            
            if blocksize>1:
                arr_10m_ref_res = blockmax(arr_10m_ref,blocksize)
                arr_10m_test_res = blockmax(arr_10m_test,blocksize)
            else:
                arr_10m_ref_res = arr_10m_ref
                arr_10m_test_res = arr_10m_test
                
            curr_blocksize_m = blocksize*orig_res
            curr_bocksize_resampled_px = int(geog_scale / float(curr_blocksize_m))
            
            shift_m=geog_scale/float(stride)
            shift_orig_cells = shift_m/float(orig_res)
            shift_target_cells = int(shift_orig_cells / blocksize)
            shifts = np.arange(0,curr_bocksize_resampled_px,shift_target_cells)
            reftiles=[]                              
            for i in shifts:
                for j in shifts:
                    tiles_y = np.array_split(arr_10m_ref_res[i:,j:],int(arr_10m_ref_res[i:,j:].shape[0]/float(curr_bocksize_resampled_px)),axis=0)
                    for tile_y in tiles_y:
                        tiles_x = np.array_split(tile_y,int(tile_y.shape[1]/float(curr_bocksize_resampled_px)),axis=1)
                        for tile_x in tiles_x:   
                            reftiles.append(tile_x.copy())
                            if np.sum(tile_x)>0:    
                                print(i,'ref',max(shifts),geog_scale,blocksize,np.sum(tile_y),np.sum(tile_x))

            testtiles=[]
            for i in shifts:
                for j in shifts:                                                                             
                    tiles_y = np.array_split(arr_10m_test_res[i:,j:],int(arr_10m_test_res[i:,j:].shape[0]/float(curr_bocksize_resampled_px)),axis=0)
                    for tile_y in tiles_y:
                        tiles_x = np.array_split(tile_y,int(tile_y.shape[1]/float(curr_bocksize_resampled_px)),axis=1)
                        for tile_x in tiles_x:   
                            testtiles.append(tile_x.copy())                        
                            if np.sum(tile_x)>0:    
                                print(i,'test',max(shifts),geog_scale,blocksize,np.sum(tile_y),np.sum(tile_x))
                        
            alltiles=list(zip(reftiles,testtiles))
            
            numtiles=len(alltiles)
            tilecount=0
            for tilepair in alltiles:
                if np.nansum(tilepair[0])==0 and np.nansum(tilepair[1])==0:
                    continue
                refvec = tilepair[0].flatten()
                testvec = tilepair[1].flatten()
                                    
                currdf=pd.DataFrame()
                currdf['ref']=refvec
                currdf['test']=testvec
                
                tp=len(currdf[np.logical_and(currdf.ref==1,currdf.test==1)])
                fp=len(currdf[np.logical_and(currdf.ref==0,currdf.test==1)])
                fn=len(currdf[np.logical_and(currdf.ref==1,currdf.test==0)])
                prec=np.divide(tp,float(tp+fp))
                rec=np.divide(tp,float(tp+fn))
                
                allfocaldata.append([geog_scale,blocksize,tp,fp,fn,prec,rec])                        
                print(tilecount,numtiles,geog_scale,blocksize,tp,fp,fn,prec,rec)
                tilecount+=1
    
    allfocaldatadf = pd.DataFrame(allfocaldata) 
    allfocaldatadf.columns=['geog_scale','blocksize','tp','fp','fn','prec','rec']               
    allfocaldatadf.to_csv('./data/focal_accmeas_multi_blocks.csv')   
    
if vis:
    allfocaldatadf=pd.read_csv('./data/focal_accmeas_multi_blocks.csv')
    fig,axs=plt.subplots(len(geog_scales),len(blocksizes),sharex=True,sharey=True,figsize=(5,5))
    scalecount=0
    for geog_scale in geog_scales:
        blocksizecount=0
        for blocksize in blocksizes:
            plotdf=allfocaldatadf[allfocaldatadf.geog_scale==geog_scale]
            plotdf=plotdf[plotdf.blocksize==blocksize]
            plotdf['refbudens']=np.log(1+(plotdf.tp+plotdf.fn))
            ax=axs[scalecount,blocksizecount]
            ax.scatter(plotdf.prec.values,plotdf.rec.values,s=2,alpha=0.9,c=plotdf.refbudens.values,cmap='viridis')
            ax.set_xlim([0,1])
            ax.set_ylim([0,1])
            ax.set_yticks([0,0.5,1])
            ax.set_yticklabels([0.0,0.5,1.0])
            if scalecount==2:
                ax.set_xlabel('Block size = %s' %blocksize)
            if blocksizecount==0:
                ax.set_ylabel('Support = %s' %geog_scale)
            blocksizecount+=1
        scalecount+=1
    plt.suptitle('Spatially explicit accuracy: Precision (x) vs. Recall (y)\nfor multiple analytical units and spatial support levels')
    plt.show()
    fig.savefig('./data/prec_rec_scat_sensitivity_panel.png', dpi=150)

    