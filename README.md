# Spatially explicit, scale-sensitive accuracy assessment of binary gridded datasets
A set of python scripts for spatially explicit, scale-sensitive accuracy assessments of binary, gridded geospatial data, e.g., for human settlement data mapping built-up (1) and not built-up (0) areas.

Global classification / data accuracy estimates ofteh ignore the spatial variation of accuracy within a dataset. Thie suite of scripts allows for estimating the accuracy of a gridded, binary dataset, given a reference dataset in the same spatial grid and extent, in a spatially explicit way. This includes the computation of zonal accuracy estimates based on an additional, vector-based zoning dataset, and the computation of focal accuracy estimates in (overlapping), quadratic focal windows.

Several factors may influence spatially-explicit accuracy estimates: 

(a) The analytical unit (i.e., cell size). In particular, if original spatial resolution is used, positional inaccuracies in reference and / or  test data may bias the thematic accuracy estimates due to misalignment of the gridded data. To mitigate this, blocks of e.g., 3x3 pixels are commonly used. These scripts allow to estimate accuracy for a range of block sizes.

(b) The spatial support. The spatial support defines the local sample of grid cells used to establish localized confusion matrices. These scrips allow for fast computation of localized confusion matrices based on zonal support levels (i.e., given by external zoning data) and for a range of focal support levels (i.e., quadratic blocks centered around a given center pixel).

Script overview:

- accuracy_assessment_global_multi_res.py: Calculates a global accuracy estimate at various levels of block size.
- accuracy_assessment_zonal.py: Calculates accuracy metrics within given polygonal zoning data in shapefile format. Creates a shapefile with a range of accuracy metrics appended to the input vector data.
- accuracy_assessment_focal_multi_res.py: Calculates focal accuracy estimates within a user-defined range of spatial support levels, and for a range of user-defined analytical units (i.e., block sizes). The outputs are focal accuracy estimates in a CSV file, as well as a faceted scatterplot of localized Precision and Recall, for each combination of spatial support and block size.
- accmeas.py: Contains functions to calculate accuracy / agreement metrics, to be applied via lambda functions to a pandas DataFrame holding the counts of true positives (tp), false negative (fn), etc.


These metrics include:
- Percentage correctly classified (PCC), aka overall accuracy
- Precision, Recall, F1-score
- Adjusted F-score
- Cohen's Kappa
- Intersection-over-union
- G-mean
- Matthew's correlation coefficient
- Rbsolutie error (total positive test instances - total positive reference instances)
- Relative error (total positive test instances - total positive reference instances) / total positive reference instances)
These functions can be applied like this:

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

All functions have a counterpart with suffix "_2" (e.g., pcc --> pcc_2) that allows for element-wise accuracy metric calcculation based on 1-d vectors of true positive, false negatives, etc.

accuracy_assessment_global_multi_res.py: 
<img width="1000" src="https://github.com/johannesuhl/local_accuracy/blob/main/fig1.JPG">

accuracy_assessment_zonal.py:
<img width="1000" src="https://github.com/johannesuhl/local_accuracy/blob/main/fig2.JPG">

accuracy_assessment_focal_multi_res.py: 
<img width="1000" src="https://github.com/johannesuhl/local_accuracy/blob/main/fig3.JPG">

References:

Uhl, J. H., & Leyk, S. (2022). A framework for scale-sensitive, spatially explicit accuracy assessment of binary built-up surface layers. arXiv preprint arXiv:2203.11253. https://arxiv.org/abs/2203.11253

Uhl, J. H., & Leyk, S. (2017). [Multi-Scale Effects and Sensitivities in Built-up Land Data accuracy Assessments](https://www.researchgate.net/profile/Johannes_Uhl/publication/325813529_Multi-Scale_Effects_and_Sensitivities_in_Built-up_Land_Data_Accuracy_Assessments/links/5b282a06aca2727335b6f1e5/Multi-Scale-Effects-and-Sensitivities-in-Built-up-Land-Data-Accuracy-Assessments.pdf). International Cartographic Conference, Washington D.C., USA, July, 2017.
