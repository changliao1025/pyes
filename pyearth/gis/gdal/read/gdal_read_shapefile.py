import os
import sys
import numpy as np
from osgeo import gdal, gdalconst, ogr, osr

def gdal_read_shapefile(sFilename_in):
    """
    Read a ESRI Shapefile. 
    Be careful that GDAL Python blinding has issue with some objects
    """

    sDriverName = "ESRI Shapefile"
    pDriver = ogr.GetDriverByName( sDriverName )

    if pDriver is None:
        print ("%s pDriver not available.\n" % sDriverName)
    else:
        print  ("%s pDriver IS available.\n" % sDriverName)

    pDataset = pDriver.Open(sFilename_in, gdal.GA_ReadOnly)
    
    # Check to see if shapefile is found.
    if pDataset is None:
        print ('Could not open %s' % (sFilename_in))
    else:
        

        pLayer = pDataset.GetLayer()
        lFeatureCount = pLayer.GetFeatureCount()
        print ("Number of features in %s: %d" %  (os.path.basename(sFilename_in),lFeatureCount))
        
        pSpatailRef = pLayer.GetSpatialRef() 
        
        aFeature=[]
        for pFeature in pLayer:         

            pGeometry = pFeature.GetGeometryRef()
            #print (pGeometry.Centroid().ExportToWkt())
            aFeature.append(pGeometry)       

        return aFeature, pSpatailRef, lFeatureCount