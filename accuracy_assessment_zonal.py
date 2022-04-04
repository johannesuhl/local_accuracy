# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 23:18:51 2022

@author: Johannes h. Uhl, University of Colorado Boulder, USA.
"""
import os,sys

## binary rasters, containing 1 and 0 only
test_tif = './data/test.tif' # test data
ref_tif = './data/reference.tif' # reference data
cellsize = 40 ## cell size of test_tif and ref_tif

rast_zonal=False ### requires arcpy
comp_accmeas=True ### calculates zonal accuracy measures
export_shp_vis_accmeas=True ### exports zonal accuracy measures to shapefile

zonal_datasets=[] ## a progression of one of more levels of zonal geometries, e.g., county, town, tract, block,...
zonal_datasets.append('./data/zones1.shp')
zonal_datasets.append('./data/zones2.shp')

levels=['zones1','zones2'] ## names for each zonal geometry level.

if rast_zonal:
    
    import arcpy,os
    from arcpy.sa import *
    arcpy.CheckOutExtension("Spatial")
    arcpy.env.compression = "LZW"
    arcpy.env.overwriteOutput = True
    
    arcpy.env.extent = test_tif
    arcpy.env.outputCoordinateSystem = test_tif
    arcpy.env.cellsize = test_tif
    arcpy.env.snapRaster = test_tif
    
    for zonal_dataset in zonal_datasets:    
        arcpy.PolygonToRaster_conversion(zonal_dataset,'FID',zonal_dataset.replace('.shp','.tif'),cellsize=cellsize)
        print(zonal_dataset)
   
if comp_accmeas:
    
    import gdal
    import numpy as np
    import accmeas
    import pandas as pd
    
    def calc_accmeas(df,level):
        df['pcc'] = df.apply(lambda row : accmeas.pcc(row.tp,row.tn,row.fp,row.fn), axis = 1)
        df['nmi'] = df.apply(lambda row : accmeas.nmi(row.tp,row.tn,row.fp,row.fn), axis = 1)
        df['recall'] = df.apply(lambda row : accmeas.recall(row.tp,row.tn,row.fp,row.fn), axis = 1)
        df['precision'] = df.apply(lambda row : accmeas.precision(row.tp,row.tn,row.fp,row.fn), axis = 1)
        df['kappa'] = df.apply(lambda row : accmeas.kappa(row.tp,row.tn,row.fp,row.fn), axis = 1)
        df['f1'] = df.apply(lambda row : accmeas.f1(row.tp,row.tn,row.fp,row.fn), axis = 1)
        df['gmean'] = df.apply(lambda row : accmeas.gmean(row.tp,row.tn,row.fp,row.fn), axis = 1)
        df['iou'] = df.apply(lambda row : accmeas.iou(row.tp,row.tn,row.fp,row.fn), axis = 1)
        df['f1_adjusted'] = df.apply(lambda row : accmeas.f1_adjusted(row.tp,row.tn,row.fp,row.fn), axis = 1)
        df['abs_err'] = df.apply(lambda row : accmeas.abs_err(row.tp,row.tn,row.fp,row.fn), axis = 1)
        df['rel_err'] = df.apply(lambda row : accmeas.rel_err(row.tp,row.tn,row.fp,row.fn), axis = 1)
        df['mcc'] = df.apply(lambda row : accmeas.mcc(row.tp,row.tn,row.fp,row.fn), axis = 1)
        df['refbudens']=100*(cellsize*cellsize/1000000.)*(df.tp+df.fn)/df.area_sqkm
        df['testbudens']=100*(cellsize*cellsize/1000000.)*(df.tp+df.fp)/df.area_sqkm        
        df.to_csv('zonal_accmeas_%s.csv' %level,index=False)

    test_arr = gdal.Open(test_tif).ReadAsArray()#.astype(np.int8)
    ref_arr = gdal.Open(ref_tif).ReadAsArray()#.astype(np.int8)
    cellsize=30 ## in m
    
    print(test_arr.shape)
    print(ref_arr.shape)
    
    test_arr[test_arr==15]=-9999 ### set nodata (here: 15) to -9999
    test_arr[test_arr==15]=-9999 ### set nodata (here: 15) to -9999
    
    test_bin_arr=test_arr.flatten()
    ref_bin_arr=ref_arr.flatten()
    
    tps=np.zeros(ref_bin_arr.shape)
    fps=np.zeros(ref_bin_arr.shape)
    tns=np.zeros(ref_bin_arr.shape)
    fns=np.zeros(ref_bin_arr.shape)
    
    tps[np.logical_and(ref_bin_arr==1,test_bin_arr==1)]=1
    fps[np.logical_and(ref_bin_arr==0,test_bin_arr==1)]=1
    tns[np.logical_and(ref_bin_arr==0,test_bin_arr==0)]=1
    fns[np.logical_and(ref_bin_arr==1,test_bin_arr==0)]=1
   
    tempdf=pd.DataFrame()
    tempdf['tp']=tps.astype(np.int8)
    tempdf['fp']=fps.astype(np.int8)
    tempdf['tn']=tns.astype(np.int8)
    tempdf['fn']=fns.astype(np.int8)          
    
    for zonal_dataset in zonal_datasets:
        level = levels[zonal_datasets.index(zonal_dataset)]
        zone_id_tif = zonal_dataset.replace('.shp','.tif')
        zone_arr = gdal.Open(zone_id_tif).ReadAsArray().flatten()
        print(level,zone_arr.shape)
        tempdf[level+'_id']=zone_arr
        
    tempdf = tempdf.replace(-9999,np.nan)  
    tempdf = tempdf.dropna()
    tempdf['area_sqkm'] = cellsize*cellsize/1000000.0
    
    for level in levels:    
        aggr_cat_sum_df=tempdf.groupby(level+'_id')[['tp','fp','tn','fn','area_sqkm']].sum().reset_index()    
        calc_accmeas(aggr_cat_sum_df,level)
            
if export_shp_vis_accmeas:
    import geopandas as gp
    import pandas as pd
    import matplotlib.pyplot as plt
    
    for level in levels:
        zonal_dataset = zonal_datasets[levels.index(level)]
        gdf = gp.read_file(zonal_dataset)
        gdf = gdf[['geometry']]
        gdf['id'] = gdf.index+1
        accmeas_csv='zonal_accmeas_%s.csv' %level
        accmeas_df=pd.read_csv(accmeas_csv)
        gdf = gdf.merge(accmeas_df,left_on='id',right_on='%s_id' %level)         
        ###visualize exemplary accuracy measure as choropleth map
        fig,ax=plt.subplots()
        gdf.plot(column='iou',ax=ax) ### to be expanded   
        ax.set_axis_off() 
        fig = ax.get_figure()             
        plt.tight_layout(pad=0)
        fig.savefig('./data/iou_%s.png' %level)
        ###export to shp
        gdf.to_file(zonal_dataset.replace('.shp','_wFocalAccMeasures.shp'))
        print(level)