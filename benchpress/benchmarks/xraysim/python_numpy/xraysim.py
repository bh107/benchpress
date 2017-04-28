#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on Mon Aug 31 14:14:15 2015

@author: Mads Thoudahl

"""
from xraysimphysics import emptyAAscene, addobjtoscene
from xraysimgeometry import coordsAAscene, raygeometry, detectorgeometry, runAABB
import numpy as np
from material import Material
from scene_objects import snake, man, fivecubes
from benchpress import util

class Const:
    EPS = 1e-5
    invsqr = 1.0 / (np.pi * 4)

def buildscene(
    scenedefs,      # scenedefinitions
    objlist,        # list of objects, obj=
    verbose=False   # printing status updates along the way
    ):
    """ Builds and returns a (sparse) scenegrid, and a (dense) voxel array,
        describing what materials are in which voxels

        args:
            scenedefs   in the form [x0,y0,z0,x1,y1,z1,xr,yr,zr], where
                        *0, and *1 is corners spanning axis aligned scene.
                        *r is resolution in the three dimensions.

            objectlist  list of objects in the form
                        obj = [objref, shape, material, referencesystem, specific geometric describers]

            verbose     directions to verboseprint std is False

        returns:
            scenegrid       meshgrid [np[x0..x1], np[y0..y1], np[z0..z1]]
                            list of arrays of shapes [(xr+1), (yr+1), (zr+1)]
            scenematarials  3D array of shape (xr,yr,zr) describing which
                            material inhibits which voxel in the scene """
    # create empty scene
    scenegrid = coordsAAscene(scenedefs)
    scenematerials = emptyAAscene(scenedefs)
    if verbose: print("axisaligned scene generated")

    # habitate scene with objects
    added, discarded = [], []
    for obj in objlist:
        if addobjtoscene(scenedefs, scenematerials, obj):
            added.append(obj[0])
            if verbose: print("object {} included".format(obj[0]))
        else:
            discarded.append(obj[0])
            if verbose: print("object {} NOT included".format(obj[0]))

    if verbose:
        print ("axisaligned scene inhabited with {} objects, {} discarded".format(len(added), len(discarded)))
        print ("objects added: {}".format(added))
        print ("objects discarded: {}".format(discarded))

    return scenegrid, scenematerials



def xraysim(sourcelist,
            detectordeflist,
            scenegrid,
            scenematerials,
            materials,
            scene_resolution,
            detector_resolution,
            verbose=False,
            visualize=False):
    """ performs the calculations figuring out what is detected
        INPUT:
        sourcelist: list of np.array([
                        px,py,pz,       position
                        relative_power, relative to other sources simulated
                        energy])        MeV

        detectorlist: list of np.array([
                        px0,py0,pz0,    position lower left corner
                        px1,py1,pz1,    position upper right corner
                        res1,res2 ])    resolution of detector

        scenegrid:      a numpy array 'meshgrid' shaped (xs+1,ys+1,zs+1)
                        containing absolute coordinates of grid at 'intersections'
                        as returned by buildscene

        scenematerials: a numpy array shaped (xs,ys,zs)
                        containing information of which MATERIAL inhibits
                        any voxel, as an integer value.
                        ## for a better model this should also contain
                        ## information of how much of the voxel is filled..

        materials:     a dict containing all materials used in the scenematerials
                       as Material objects

        scene_resolution:    resolution of the scene cubic, e.g. 32 equals 32^3

        detector_resolution: resolution of the detectors squared, e.g. 22 equals 22^2
    """
    ## indexing constants
    power = 3

    # generate an array of endpoints for rays (at the detector)
    detectors = []
    for ddef in detectordeflist:
        detectors.append(detectorgeometry(ddef))

    for source in sourcelist:
        # unpack source
        sx, sy, sz, spower, senergy = source
        rayorigin = sx, sy, sz

        # preprocess the scene physics
        # building a map of attenuation coefficients
        sceneattenuates =  np.zeros(scenematerials.shape)

        for material_id in materials.keys():
            sceneattenuates += (scenematerials == material_id) \
                    * materials[material_id].getMu(senergy)

        ret = []
        for pixelpositions, pixelareavector, dshape, result in detectors:
            # do geometry
            rayudirs, raylengths, rayinverse = raygeometry(rayorigin, pixelpositions)
            raydst = runAABB(scenegrid, rayudirs, rayorigin, rayinverse)

            #raydst is now to be correlated with material/attenuation grid
            t = sceneattenuates[...,np.newaxis] * raydst
            #We sums the three dimensions
            t = np.sum(t, axis=(0, 1, 2))
            dtectattenuates = t.reshape(detector_resolution, detector_resolution)
            pixelintensity = ((Const.invsqr * source[power] * np.ones(raylengths.shape[0])[..., np.newaxis]) / raylengths).reshape(dshape)
            area = np.dot( rayudirs, pixelareavector.reshape(3,1) ).reshape(dshape)
            result += pixelintensity * area * np.exp(-dtectattenuates)
            ret.append(result)
            if visualize:
                low = np.minimum.reduce(result.flatten())
                high = np.maximum.reduce(result.flatten())
                if util.Benchmark().bohrium:
                    low  = low.copy2numpy()
                    high = high.copy2numpy()
                util.plot_surface(result, "2d", 0, low-0.001*low, high-0.5*high)
                util.plot_surface(result, "2d", 0, low-0.001*low, high-0.5*high)

    #We return only the result of the detectors
    return ret

def setup(scene_res, detector_res):
    """Returns a scene to xray

       scene_res:    resolution of the scene cubic, e.g. 32 equals 32^3
       detector_res: resolution of the detectors squared, e.g. 22 equals 22^2
    """

    srclist, detectorlist, scenedefs, objectlist = snake(scene_res, detector_res)

    # build a model of all materials
    materials = Material.initAll()

    # build scene
    scenegrid, scenematerials = buildscene(scenedefs, objectlist)

    return (srclist, detectorlist, scenegrid, scenematerials, materials, scene_res, detector_res)

def main():
    B = util.Benchmark()
    scene_res = B.size[0]
    detector_res = B.size[1]
    iterations = B.size[2]
    scene = setup(scene_res, detector_res)

    B.start()
    for _ in range(iterations):
        detector_results = xraysim(*scene, visualize=B.visualize)
        if util.Benchmark().bohrium:
            B.flush()

    B.stop()
    B.pprint()

    if B.outputfn:
        B.tofile(B.outputfn, {'res': detector_results[0]})

    if B.visualize:
        util.confirm_exit()

if __name__ == '__main__':
    main()
