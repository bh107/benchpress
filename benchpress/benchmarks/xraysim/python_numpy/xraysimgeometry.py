# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 14:38:12 2015

@author: Mads Thoudahl

"""
import numpy as np

## for enumeration purposes
class Shape:
    cube   = 0
    sphere = 1

class Reference:
    absolute = 0
    relative = 1


def coordsAAscene(scenedefs):
    """ returns a meshgrid of the scene coordinates from its definitions
        forming an AxisAligned scene

        args:
            definitions:   [x0,y0,z0,  scene corner 0
                            x1,y1,z1,  scene corner 1
                            xr,yr,zr]  scene resolutions
        returns:
            meshgrid:      [ np(x0..x1), np(y0..y1), np(z0..z1) ]
                             of lengths [ xr+1, yr+1, zr+1 ] """
    x0, y0, z0 = scenedefs[0:3] # position lower left
    x1, y1, z1 = scenedefs[3:6] # position upper right
    xres, yres, zres = scenedefs[6:9] # resolution

    xgrid = np.linspace(x0, x1, (xres+1))
    ygrid = np.linspace(y0, y1, (yres+1))
    zgrid = np.linspace(z0, z1, (zres+1))

    return np.meshgrid(xgrid,ygrid,zgrid)


def raygeometry(src, detpixpos):
    """ calculates an array of normalized (length=1) vectors representing
        geometric ray directions, from the source and detector
        pixel positions

        args:
            src          is source position
            detpixpos    is a 3D array, 2 pixel dimensions,
                         one spatial xyz positions
        returns:
            unitrays     is the ray directions in unit lengths,
                         flattened to 1 pixel dimension, and 1 spatial dimension
            distances    is the distances belonging to the ray-vector
            rayinverses  serves to minimize division operations
        """
    rayshp         = detpixpos.shape
    raycount       = rayshp[0]*rayshp[1]
    origin         = np.array([src[0],src[1],src[2]])
    rays           = detpixpos.reshape(raycount,3)[:,0:3] - origin

    raydistances   = np.sqrt(np.sum(rays*rays, axis=1)).reshape(raycount,1)
    unitrays       = rays / raydistances

    rayinverses    = np.ones(unitrays.shape) / unitrays
    return  unitrays, raydistances, rayinverses


def detectorgeometry(ddef):#, npdtype='float64'):
    """ calculates the geometric properties of the detector
        from its definitions

        args:
            ddef is array detector definitions

        returns:
            pixelpositions    The endpoint of all the vectors
            unitnormalvector  of the detector  """
    c0 = np.array([ddef[0],ddef[1],ddef[2]]) # corner c1-c0-c2
    c1 = np.array([ddef[3],ddef[4],ddef[5]]) # corner c0-c1-c3 or 1st axis endposition
    c2 = np.array([ddef[6],ddef[7],ddef[8]]) # corner c0-c2-c3 or 2nd axis endposition
    r1 = ddef[9]   # resolution in 1st dimension
    r2 = ddef[10]  # resolution in 2nd dimension

    dshape = (r2,r1)  # CONTROL of SEQUENCE
    # unit direction vectors of detector sides
    di = (c1 - c0) * (1.0/r1)
    dj = (c2 - c0) * (1.0/r2)
    def pcfun(j,i,k): return  c0[k] + (i+0.5) * di[k] + (j+0.5) * dj[k]
    def pcfunx(j,i):  return pcfun(j,i,0)
    def pcfuny(j,i):  return pcfun(j,i,1)
    def pcfunz(j,i):  return pcfun(j,i,2)
    pxs  = np.fromfunction(pcfunx, shape=dshape)#, dtype=npdtype )
    pys  = np.fromfunction(pcfuny, shape=dshape)#, dtype=npdtype )
    pzs  = np.fromfunction(pcfunz, shape=dshape)#, dtype=npdtype )
    pixelpositions = np.array(np.dstack((pxs,pys,pzs))) # shape = (r2,r1,3)

    pixelareavector = np.array(np.cross(di, dj))
    result = np.zeros(dshape)

    return  pixelpositions, pixelareavector, dshape, result


def fmin(a, b):
    return a * (a <= b) + b * (b < a)

def fmax(a, b):
    return a * (a >= b) + b * (b > a)

def runAABB( scenegrid,
             rayudirs,
             rayorigin,
             rayinverse
             ):
    """ Core AxisAlignedBoundingBox intersection algorithm, extended to
        return the distances that every ray travels in every voxel

        args:
          scenegrid           3D meshgrid, a list of 3 arrays shaped:
                              [(rx+1),(ry+1),(rz+1)]  - (r* is scene * resolution)

          rayudirs            unit direction vector (|uv|==1) for all rays
                              going from rayorigin to the detector
                              array shaped (rda*rdb,3)
                              where rda,rdb is resolution of detector in a,b direction

          rayorigin           origin coordinate for all rays
                              as a 1D array (x0,y0,z0)

          rayinverse          array shaped (rda*rdb,3) really just 1/rayudirs

        returns:
          voxelraydistances   a voxelgrid per ray, shape (rx,ry,rz,rda*rdb)
                              containing the distances every ray travels in
                              every grid
        """

    txs0 = ( scenegrid[0][:-1,:-1,:-1, np.newaxis] - rayorigin[0] ) * rayinverse[:,0]
    txs1 = ( scenegrid[0][1:,1:,1:   , np.newaxis] - rayorigin[0] ) * rayinverse[:,0]

    tys0 = ( scenegrid[1][:-1,:-1,:-1, np.newaxis] - rayorigin[1] ) * rayinverse[:,1]
    tys1 = ( scenegrid[1][1:,1:,1:   , np.newaxis] - rayorigin[1] ) * rayinverse[:,1]

    tzs0 = ( scenegrid[2][:-1,:-1,:-1, np.newaxis] - rayorigin[2] ) * rayinverse[:,2]
    tzs1 = ( scenegrid[2][1:,1:,1:   , np.newaxis] - rayorigin[2] ) * rayinverse[:,2]

    t_in  = fmax(fmin(txs0, txs1), fmax(fmin(tys0, tys1), fmin(tzs0, tzs1)))
    t_out = fmin(fmax(txs0, txs1), fmin(fmax(tys0, tys1), fmax(tzs0, tzs1)))

    voxelraydistances = (t_out-t_in)*(t_out>=t_in)
    return voxelraydistances
