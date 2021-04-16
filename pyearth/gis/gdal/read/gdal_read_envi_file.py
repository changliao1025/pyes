import os, sys
import numpy as np
from osgeo import gdal, osr,ogr,  gdalconst


def gdal_read_envi_file(sFilename_in):
    """Read a ENVI standard format raster file."""

    sDriverName='ENVI'
    pDriver = ogr.GetDriverByName(sDriverName)  

    if pDriver is None:
        print ("%s pDriver not available.\n" % sDriverName)
    else:
        print  ("%s pDriver IS available.\n" % sDriverName)
         
    pDataset = pDriver.Open(sFilename_in, gdal.GA_ReadOnly)

    if pDataset is None:
        print("Couldn't open this file: " + sFilename_in)
        print('Perhaps you need an ENVI .hdr file?')
        
        sys.exit("Try again!")
    else:
        
        pProjection = pDataset.GetProjection()
       
        ncolumn = pDataset.RasterXSize
        nrow = pDataset.RasterYSize
        nband = pDataset.RasterCount

        pGeotransform = pDataset.GetGeoTransform()
        dOriginX = pGeotransform[0]
        dOriginY = pGeotransform[3]
        pPixelWidth = pGeotransform[1]
        pPixelHeight = pGeotransform[5]
       
        pBand = pDataset.GetRasterBand(1)
        dMissing_value = pBand.GetNoDataValue()
        aData_out = pBand.ReadAsArray(0, 0, ncolumn, nrow)
        pSpatialRef = osr.SpatialReference(wkt=pProjection)

        pDriver = None
        pDataset = None
        pBand = None

        return aData_out, pPixelWidth, dOriginX, dOriginY, nrow, ncolumn, dMissing_value , pGeotransform, pProjection,  pSpatialRef


def gdal_read_envi_file_multiple_band(sFilename_in):
    """Read a ENVI standard format raster file with multiple bands."""

    sDriverName='ENVI'
    pDriver = ogr.GetDriverByName(sDriverName)  

    if pDriver is None:
        print ("%s pDriver not available.\n" % sDriverName)
    else:
        print  ("%s pDriver IS available.\n" % sDriverName) 

    pDataset = pDriver.Open(sFilename_in, gdal.GA_ReadOnly)

    if pDataset is None:
        print("Couldn't open this file: " + sFilename_in)
        print('Perhaps you need an ENVI .hdr file?')
        
        sys.exit("Try again!")
    else:
        
        pProjection = pDataset.GetProjection()
       
        ncolumn = pDataset.RasterXSize
        nrow = pDataset.RasterYSize
        nband = pDataset.RasterCount

        pGeotransform = pDataset.GetGeoTransform()
        dOriginX = pGeotransform[0]
        dOriginY = pGeotransform[3]
        pPixelWidth = pGeotransform[1]
        pPixelHeight = pGeotransform[5]

        pBand = pDataset.GetRasterBand(1)
        dt = gdal.GetDataTypeName(pBand.DataType)
        dMissing_value = pBand.GetNoDataValue()
        #there is a chance that GDAL datetype is not compatiable with numpy datatype.

        aData_out = np.full( (nband, nrow, ncolumn) , -9999.0, dtype= dt )
        for iBand in range(nband):
            pBand = pDataset.GetRasterBand( iBand + 1)
            
            aData_out[iBand, :, :] = pBand.ReadAsArray(0, 0, ncolumn, nrow)

        pSpatialRef = osr.SpatialReference(wkt=pProjection)

        pDriver = None
        pDataset = None
        pBand = None

        return aData_out, pPixelWidth, dOriginX, dOriginY, nband, nrow, ncolumn, dMissing_value , pGeotransform, pProjection, pSpatialRef