#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on Mon Aug 31 14:14:15 2015

@author: Mads Thoudahl

"""

import numpy as np

from xraysimgeometry import Shape, Reference
from material import Material

SSX             = 22
SSY             = 22
SSZ             = 22

ARES            = 32
BRES            = 32


def fivecubes():
    """ creates a 2 small boxes within a bigger box in the lower left corner of the detector  """
    # DEFINING THE EXPERIMENTAL SETUP, THE SOURCE, SCENE AND DETECTOR DEFINITIONS
    asource   = [
                  0.5, 0.5, 0.0,     # position
                  1,                 # Power [relative to other sources]
                  0.080              # Energy level of xrays [MeV] 0.080
                ]

    scenedefs = [
                  0.2, 0.2, 1.2,     # position lower left
                  0.8, 0.8, 1.8,     # position upper right
                  SSX,               # resolution1 (#pixels)
                  SSY,               # resolution2 (#pixels)
                  SSZ                # resolution3 (#pixels)
                ]                    # voxelcount = res1 * res2 * res3

    adetector = [                    # rectangular surface spanned by 3 points, 2 resolutions
                   0.0,  0.0,  2.0,  # corner 0 position
                   0.0,  1.0,  2.0,  # corner h2 position
                   1.0,  0.0,  2.0,  # corner h1 position
                  ARES,              # resolution1 (#pixels)
                  BRES               # resolution2 (#pixels)
                ]


    # DEFINING THE SCENE SETUP, HOW THE OBJECTS IN THE EXPERIMENT ARE PLACED
    # SHAPED, AND WHAT MATERIALS THEEY ARE MADE FROM

    o1  = [ 1,                       # Object reference number
            Shape.cube,              # Shape
            Material.muscle,       # Material from which it consists
            Reference.relative,      # Reference point of view
            [np.array([2,2,2]),      # Shape specific geometric characteristics
             np.array([18,18,12])]
          ]

    o2 =  [ 2,                       # Object reference number
            Shape.cube,              # Shape
            Material.hydrogen,       # Material from which it consists
            Reference.absolute,      # Reference point of view
            [[0.3,0.3,1.3],          # Shape specific geometric characteristics
             [0.4,0.4,1.4]]
          ]

    o3  = [ 3,                       # Object reference number
            Shape.cube,              # Shape
            Material.bone,       # Material from which it consists
            Reference.relative,      # Reference point of view
            [np.array([3,3,3]),      # Shape specific geometric characteristics
             np.array([6,6,5])]
          ]

    o4  = [ 4,                       # Object reference number
            Shape.cube,              # Shape
            Material.pe,       # Material from which it consists
            Reference.relative,      # Reference point of view
            [np.array([10,10,5]),   # Shape specific geometric characteristics
             np.array([12,12,7])]
          ]

    o5  = [ 5,                       # Object reference number
            Shape.cube,              # Shape
            Material.tissue,       # Material from which it consists
            Reference.relative,      # Reference point of view
            [np.array([8,3,8]),      # Shape specific geometric characteristics
             np.array([10,6,10])]
          ]

    return ([asource], [adetector], scenedefs, [o1,o2,o3,o4,o5])




def man():
    """ creates a man shaped figure with skeleton and all, and a couple of artifacts  """
    # DEFINING THE EXPERIMENTAL SETUP, THE SOURCE, SCENE AND DETECTOR DEFINITIONS

    asource   = [
                  0.5, 1.0, 0.0,     # position
                  1,                 # Power [relative to other sources]
                  0.080              # Energy level of xrays [MeV] 0.080
                ]

    scenedefs = [
                  0.0, 0.0, 1.0,     # position lower left
                  1.0, 2.0, 1.5,     # position upper right
                  SSX,               # resolution1 (#pixels)
                  SSY,               # resolution2 (#pixels)
                  SSZ                # resolution3 (#pixels)
                ]                    # voxelcount = res1 * res2 * res3

    adetector = [                    # rectangular surface spanned by 3 points, 2 resolutions
                   0.0,  0.0,  1.6,  # corner 0 position
                   0.0,  2.5,  1.6,  # corner h2 position
                   1.5,  0.0,  1.6,  # corner h1 position
                  ARES,              # resolution1 (#pixels)
                  BRES               # resolution2 (#pixels)
                ]


    # DEFINING THE SCENE SETUP, HOW THE OBJECTS IN THE EXPERIMENT ARE PLACED
    # SHAPED, AND WHAT MATERIALS THEEY ARE MADE FROM


    lleg = [ 1,                      # Object reference number
            Shape.cube,              # Shape
            Material.muscle,         # Material from which it consists
            Reference.relative,      # Reference point of view
            [np.array([4,0,2]),      # Shape specific geometric characteristics
             np.array([9,9,18])]
          ]

    rleg  = [ 2,                       # Object reference number
            Shape.cube,              # Shape
            Material.muscle,       # Material from which it consists
            Reference.relative,      # Reference point of view
            [np.array([16,0,2]),      # Shape specific geometric characteristics
             np.array([21,9,18])]
          ]

    torso  = [ 3,                       # Object reference number
            Shape.cube,              # Shape
            Material.muscle,       # Material from which it consists
            Reference.relative,      # Reference point of view
            [np.array([6,6,2]),   # Shape specific geometric characteristics
             np.array([19,18,18])]
          ]

    head  = [ 4,                       # Object reference number
            Shape.cube,              # Shape
            Material.muscle,       # Material from which it consists
            Reference.relative,      # Reference point of view
            [np.array([9,18,2]),   # Shape specific geometric characteristics
             np.array([16,23,18])]
          ]

    arms  = [ 5,                       # Object reference number
            Shape.cube,              # Shape
            Material.muscle,       # Material from which it consists
            Reference.relative,      # Reference point of view
            [np.array([1,15,2]),   # Shape specific geometric characteristics
             np.array([24,19,18])]
          ]

    llegb  = [ 11,                       # Object reference number
            Shape.cube,              # Shape
            Material.bone,       # Material from which it consists
            Reference.relative,      # Reference point of view
            [np.array([6,1,9]),      # Shape specific geometric characteristics
             np.array([7,8,11])]
          ]

    rlegb  = [ 12,                       # Object reference number
            Shape.cube,              # Shape
            Material.bone,       # Material from which it consists
            Reference.relative,      # Reference point of view
            [np.array([18,1,9]),      # Shape specific geometric characteristics
             np.array([19,8,11])]
          ]

    hip  = [ 13,                       # Object reference number
            Shape.cube,              # Shape
            Material.bone,       # Material from which it consists
            Reference.relative,      # Reference point of view
            [np.array([7,7,9]),      # Shape specific geometric characteristics
             np.array([18,8,11])]
          ]

    spine  = [ 14,                       # Object reference number
            Shape.cube,              # Shape
            Material.bone,       # Material from which it consists
            Reference.relative,      # Reference point of view
            [np.array([12,7,9]),      # Shape specific geometric characteristics
             np.array([13,19,11])]
          ]

    skull  = [ 15,                       # Object reference number
            Shape.cube,              # Shape
            Material.bone,       # Material from which it consists
            Reference.relative,      # Reference point of view
            [np.array([10,19,6]),      # Shape specific geometric characteristics
             np.array([15,21,15])]
          ]

    armsb  = [ 16,                       # Object reference number
            Shape.cube,              # Shape
            Material.bone,       # Material from which it consists
            Reference.relative,      # Reference point of view
            [np.array([2,16,9]),      # Shape specific geometric characteristics
             np.array([23,17,11])]
          ]

    radio  = [ 21,                       # Object reference number
            Shape.cube,              # Shape
            Material.pe,       # Material from which it consists
            Reference.relative,      # Reference point of view
            [np.array([8,7,18]),      # Shape specific geometric characteristics
             np.array([10,10,20])]
          ]

    gun1  = [ 21,                       # Object reference number
            Shape.cube,              # Shape
            Material.pe,       # Material from which it consists
            Reference.relative,      # Reference point of view
            [np.array([15,6,0]),      # Shape specific geometric characteristics
             np.array([16,10,1])]
          ]

    gun2  = [ 21,                       # Object reference number
            Shape.cube,              # Shape
            Material.pe,       # Material from which it consists
            Reference.relative,      # Reference point of view
            [np.array([15,9,0]),      # Shape specific geometric characteristics
             np.array([18,10,1])]
          ]

    objects = [lleg, rleg, torso, head, arms]
    objects.extend([llegb, rlegb, hip, spine, skull, armsb]) ## bones
    objects.extend([gun1, gun2, radio]) # items

    return ([asource], [adetector], scenedefs, objects)


def snake(scen_res=22, detector_res=32):
    """ creates a 2 small boxes within a bigger box in the lower left corner of the detector  """
    # DEFINING THE EXPERIMENTAL SETUP, THE SOURCE, SCENE AND DETECTOR DEFINITIONS
    asource   = [
                  0.5, 0.5, 0.0,     # position
                  1,                 # Power [relative to other sources]
                  0.080              # Energy level of xrays [MeV] 0.080
                ]

    scenedefs = [
                  0.2, 0.2, 1.2,     # position lower left
                  0.8, 0.8, 1.8,     # position upper right
                  scen_res,          # resolution1 (#pixels)
                  scen_res,          # resolution2 (#pixels)
                  scen_res           # resolution3 (#pixels)
                ]                    # voxelcount = res1 * res2 * res3

    adetector = [                    # rectangular surface spanned by 3 points, 2 resolutions
                   0.0,  0.0,  2.0,  # corner 0 position
                   0.0,  1.0,  2.0,  # corner h2 position
                   1.0,  0.0,  2.0,  # corner h1 position
                  detector_res,      # resolution1 (#pixels)
                  detector_res       # resolution2 (#pixels)
                ]


    # DEFINING THE SCENE SETUP, HOW THE OBJECTS IN THE EXPERIMENT ARE PLACED
    # SHAPED, AND WHAT MATERIALS THEEY ARE MADE FROM

    o0 =  [ 0,                       # Object reference number
            Shape.cube,              # Shape
            Material.blood,          # Material from which it consists
            Reference.absolute,      # Reference point of view
            [[0.2, 0.2, 1.2],        # Shape specific geometric characteristics
             [0.8, 0.8, 1.5]]
          ]

    o1 =  [ 1,                       # Object reference number
            Shape.cube,              # Shape
            Material.pe,             # Material from which it consists
            Reference.absolute,      # Reference point of view
            [[0.70, 0.25, 1.25],     # Shape specific geometric characteristics
             [0.75, 0.75, 1.35]]
          ]

    o2 =  [ 2,                       # Object reference number
            Shape.cube,              # Shape
            Material.bone,           # Material from which it consists
            Reference.absolute,      # Reference point of view
            [[0.3, 0.25, 1.25],      # Shape specific geometric characteristics
             [0.7, 0.35, 1.35]]
          ]

    o3 =  [ 3,                       # Object reference number
            Shape.cube,              # Shape
            Material.pe,             # Material from which it consists
            Reference.absolute,      # Reference point of view
            [[0.25, 0.25, 1.25],     # Shape specific geometric characteristics
             [0.30, 0.35, 1.75]]
          ]

    o4 =  [ 4,                       # Object reference number
            Shape.cube,              # Shape
            Material.bone,           # Material from which it consists
            Reference.absolute,      # Reference point of view
            [[0.25, 0.25, 1.65],      # Shape specific geometric characteristics
             [0.30, 0.75, 1.75]]
          ]

    o5 =  [ 5,                       # Object reference number
            Shape.cube,              # Shape
            Material.pe,             # Material from which it consists
            Reference.absolute,      # Reference point of view
            [[0.30, 0.65, 1.65],     # Shape specific geometric characteristics
             [0.45, 0.75, 1.75]]
          ]

    o6 =  [ 6,                       # Object reference number
            Shape.cube,              # Shape
            Material.bone,           # Material from which it consists
            Reference.absolute,      # Reference point of view
            [[0.45, 0.4, 1.30],      # Shape specific geometric characteristics
             [0.55, 0.5, 1.65]]
          ]

    o7 =  [ 7,                       # Object reference number
            Shape.cube,              # Shape
            Material.tissue,         # Material from which it consists
            Reference.absolute,      # Reference point of view
            [[0.45, 0.35, 1.30],     # Shape specific geometric characteristics
             [0.55, 0.55, 1.65]]
          ]

    return ([asource], [adetector], scenedefs, [o0,o1,o2,o3,o4,o5,o6,o7])

