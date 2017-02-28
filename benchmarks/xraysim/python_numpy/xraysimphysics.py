# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 14:37:10 2015

@author: Mads Thoudahl

"""
import numpy as np
from xraysimgeometry import Shape, Reference


def emptyAAscene( scenedefs ):
    """ Generates an AxisAligned scene, of a 3 dimensional array of voxels,
        containing vacuum (Material.vacuum == 0) in all voxels.

        Model: all boxes are *fully* occupied by exactly one (1)
               material, vacuum (Material.vacuum=0) represents zero
               attenuation """
    shp = xr, yr, zr = scenedefs[6:9] # resolution
    return np.zeros(shp)


def addobjtoscene(scene, matscene, obj):
    shape           = obj[1]
    material        = obj[2]
    reference       = obj[3]
    shapedescribers = obj[4]
    if shape == Shape.cube:
        return addAAcube(scene, matscene, shapedescribers, material, reference)
    else:
        print ("Cube shaped objects are the only ones supported at this time")
        print ("Object dropped")



def addAAcube( scene,
               matscene,
               describers,
               material,
               ref=Reference.relative,
               verbose=False ):
    """ adds a cubic shape to scene, REPLACING any material in same voxel

        scene:         scene definition metadata
                       [x0, y0, z0,   AAscene mincorner
                        x1, y1, z1,   AAscene maxcorner
                        xr, yr, zr]   resolutions in 3 dimension

        matscene:      voxel array shaped (xr,yr,zr) containing materials
        cubedescribers:
          mincorner:   reference dependant startpoint in space
          maxcorner:   reference dependant endpoint in space
        material:      Integer from Material Class (enumerator)
        ref:           input argument refer to the following
                       Reference.relative    resolution relative references
                       Reference.absolute    'real world' coordinate references

       returns:        Bool - success
                       changes materialscene as sideeffect
       """
    mincorner, maxcorner = describers
    if ref == Reference.relative:
        x0,y0,z0 = mincorner.astype(np.int64)
        x1,y1,z1 = maxcorner.astype(np.int64)
        sshp = np.array(matscene.shape, dtype=np.int)
        # guard if relative corners are bigger than scene
        x0 = x0 if x0 < sshp[0] else sshp[0]
        y0 = y0 if y0 < sshp[1] else sshp[1]
        z0 = z0 if z0 < sshp[2] else sshp[2]
        x1 = x1 if x1 < sshp[0] else sshp[0]
        y1 = y1 if y1 < sshp[1] else sshp[1]
        z1 = z1 if z1 < sshp[2] else sshp[2]

        # guard if relative corners are smaller than 0
        x0 = x0 if x0 >= 0 else 0
        y0 = y0 if y0 >= 0 else 0
        z0 = z0 if z0 >= 0 else 0
        x1 = x1 if x1 >= 0 else 0
        y1 = y1 if y1 >= 0 else 0
        z1 = z1 if z1 >= 0 else 0

        matscene[x0:x1,y0:y1,z0:z1] = material
        return True

    if ref == Reference.absolute:
        #conversion to relative coordinates and recursive call
        if verbose: print("addAAcube: adding a cube with absolute coordinates, experimental stage.")
        # f: x -> x_r  x_r = floor( (x - x0)/dx )
        def x_r(x, x0, x1, xr):
            dx = 1.0 * (x1 - x0) / xr
            return np.floor( (x-x0)/dx )

        # fetching boundary conditions from scene
        x0, x1, xr = np.array(scene[0:3]), np.array(scene[3:6]), np.array(scene[6:9])

        rel_mincorner  = x_r( np.array(mincorner), x0, x1, xr )
        rel_maxcorner  = x_r( np.array(maxcorner), x0, x1, xr )

        rel_describers = (rel_mincorner, rel_maxcorner)

        return addAAcube( scene, matscene, rel_describers, material, Reference.relative, verbose )

    return False
