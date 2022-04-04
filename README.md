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
