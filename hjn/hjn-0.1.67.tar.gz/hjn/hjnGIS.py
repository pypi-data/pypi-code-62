from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from hjn.mkNCHJN import envelope
import numpy as np
import netCDF4 as nc
import copy
import geopandas as gpd

class maskClip():
    def __init__(self,data,latAtt,lonArr,step):

        self.dem = data
        self.latArr = latAtt
        self.lonArr = lonArr

        oriStep=np.abs((self.latArr[0]-self.latArr[-1])/(len(self.latArr)-1))
        range=int(np.round(step/oriStep,0))
        self.dem=self.dem[::range,::range]

        self.ltc = envelope(self.latArr[0], self.latArr[-1], self.lonArr[0], self.lonArr[-1])
        self.step = step

    def world2Pixel(self,ltc, x, y):
        """
        Uses a gdal geomatrix (gdal.GetGeoTransform()) to calculate
        the pixel location of a geospatial coordinate
        """
        ulX = ltc.w
        ulY = ltc.n
        xDist = self.step

        pixel = int((x - ulX) / xDist)
        line = int((ulY - y) / xDist)
        return (pixel, line)


    def getMask(self,geom,minX,maxY,minY,maxX):

        points = []
        pixels = []
        ulX, ulY = self.world2Pixel(self.ltc, minX, maxY)
        lrX, lrY = self.world2Pixel(self.ltc, maxX, minY)

        # Calculate the pixel size of the new image
        pxWidth = int(lrX - ulX)
        pxHeight = int(lrY - ulY)

        ltc1 = copy.copy(self.ltc)
        ltc1.n = maxY
        ltc1.w = minX

        pts = geom.boundary.xy
        for p in range(len(pts[0])):
            points.append((pts[0][p], pts[1][p]))
        for p in points:
            pixels.append(self.world2Pixel(ltc1, p[0], p[1]))
        rasterPoly = Image.new("L", (pxWidth, pxHeight), 1)
        rasterize = ImageDraw.Draw(rasterPoly)
        if len(pixels) > 1:
            rasterize.polygon(pixels, 0)

        mask = np.asarray(rasterPoly)


        # plt.imshow(mask)
        # plt.show()

        latOffset0 = int((self.ltc.n - maxY) / self.step)
        latOffset1 = self.dem.shape[0] - int((self.ltc.n - minY) / self.step)
        lonOffset0 = int((minX - self.ltc.w) / self.step)
        lonOffset1 = self.dem.shape[1] - int((maxX - self.ltc.w) / self.step)
        ndarray = np.pad(mask, ((latOffset0, latOffset1),
                                (lonOffset0, lonOffset1)), 'constant', constant_values=(1, 1))

        clip = copy.copy(self.dem)

        clip[ndarray != 0] = np.nan

        return clip



    def clip(self,shapefile_path,encoding='gb18030'):
        chly = gpd.GeoDataFrame.from_file(shapefile_path, encoding=encoding).geometry

        minX, maxX, minY, maxY = chly.bounds.min().minx,chly.bounds.max().maxx,chly.bounds.min().miny,chly.bounds.max().maxy
        maskArr=[]

        for j in range(len(chly)):
            geom = chly[j]
            if geom.geometryType() == 'Polygon':
                clip=self.getMask(geom, minX, maxY, minY, maxX)
                maskArr.append(clip)
            elif geom.geometryType() == "MultiPolygon":
                multiLayer = []
                for i in range(len(geom)):
                    geom1 = geom[i]
                    clip = self.getMask(geom1, minX, maxY, minY, maxX)
                    multiLayer.append(clip)

                multiLayer= np.asarray(multiLayer)
                clip = np.nanmax(multiLayer,axis=0)
                maskArr.append(clip)

        return maskArr

