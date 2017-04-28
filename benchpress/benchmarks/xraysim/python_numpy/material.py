# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 09:10:36 2014
@author: Mads Thoudahl
"""

import os
from numpy import loadtxt, logspace
try:
    from cPickle import load, dump
except:
    from pickle import load, dump

class Material():
    """ Material class, representing all materials """
    # for enumeration purposes
    vacuum    = 0

    hydrogen  = 1
    carbon    = 6
    aluminium = 13
    titanium  = 22
    iron      = 26
    gold      = 79

    air       = 801
    blood     = 802
    bone      = 803
    brain     = 804
    muscle    = 805
    tissue    = 806
    cam       = 821
    oak       = 822
    pe        = 851
    # a .csv file exists for everyone of these materials.

    uids = {}  # unique ids, held at no protection, so peacul environment anticipated
    full_path = os.path.realpath(__file__)
    exec_path, exec_filename = os.path.split(full_path)
    elmpath = exec_path + '/materials/elemental'
    biopath = exec_path + '/materials/biotic'
    def __init__(self,
                 filename,  # csv file containing the measurepoints of this material
                 density=0  # material density in g/cm3
                 ):
        """ instantiate a material object from a csv file,
            structured line-wise:
            1:  'Name', *material-name*
            2:  'Z', *elemental atomic number*
            3:  'rho (g/cm3)', *standard material density @ 1 atm, 20 deg C*
            4:  'Energy (MeV)', 'mu/rho (cm2/g)'
            5:  *measurepoints sorted by energy!*
        """
        try:
            self.short  = filename[:-4] # name, shorthand

            # get name, atomic number and standard density
            f         = open(filename, "r")
            self.name = f.readline().split(',')[1].strip().strip('"')
            z         = int( f.readline().split(',')[1] )
            self.uid  = Material.uniqueid(self, z)
            if self.uid == -1:
                raise ValueError('{} does not have a new Unique ID (Z) (or has been initialized before).'.format(self.name))

            self.rho = float( density if density else f.readline().split(',')[1] )
            f.close()

            # get datapoints from file for spline interpolation
            x = loadtxt(fname=filename, delimiter=',', skiprows=4, usecols=(0,1))
            self.Es = x[:,0]
            self.mus = x[:,1] * self.rho

            self.mu = {}

        except ValueError as e:
            print(e)
            return None


    @staticmethod
    def uniqueid(self, uid):
        """ Checks if uid is vacant, if so occupies it.
            returns unique id, or -1 on error """
        if uid in Material.uids:
            return -1
        else:
            Material.uids[uid] = True
            return uid



    def __str__(self):
        """ returns a string describing this material """
        return self.name

    def getMu(self, energy):
        """ returns the absorption coefficient for this material at a
            certain energy level """

        # load/store Optimization
        try:
            # get stored mu as chances are the same has been calculated before
            return self.mu[energy]
        except (KeyError, TypeError) as e:
            e = e
            pass

        # use cubic interpolation functionto determine mu
        # fun = interp1d( self.Es, self.mus, kind='cubic')
        # NO CAN DO... DUE TO OSCILATIONS IT DOES NOT YIELD THE CORRECT RESULT
        #fun = interp1d( self.Es, self.mus, kind='linear')
        #mu = fun(energy)

        # Linear spline interpolation, self-implemented
        for i in range(len(self.Es)-1)[::-1]:
            if energy - self.Es[i] >= 0: break
        mu = self.mus[i] + (energy - self.Es[i]) * \
             ( (self.mus[i+1] - self.mus[i]) / (self.Es[i+1] - self.Es[i]) )

        # store calculated mu value and return it
        try:
            self.mu[energy] = mu
        except (KeyError, TypeError) as e:
            e = e
            pass
        return mu


    @staticmethod
    def initGroup(path):
        """ initiating all elemental materials in csv files in path """
        try:
            with open('data', 'rb') as fp:
                data = load(fp)
            return data
        except IOError:
            data  = {}
            for file_ in os.listdir( path ):
                if file_.endswith(".csv"):
                    mat = Material( path + '/' + file_ )
                    if mat is None:
                        print("{} failed to initialize".format(file_))
                    data[mat.uid] = mat
        return data

    @staticmethod
    def initAll():
        """ initiating all elemental materials in csv files in path """
        materials = { 0 : Simplemat(name = 'Vacuum', mu = 0, uid = 0) }
        materials.update( Material.initElementals() )
        materials.update( Material.initBiotics() )
        return materials

    @staticmethod
    def initElementals():
        """ initiating all elemental materials in csv files in path """
        return Material.initGroup(Material.elmpath)

    @staticmethod
    def initBiotics():
        """ initiating all elemental materials in csv files in path """
        return Material.initGroup(Material.biopath)



class Simplemat(Material):
    """ Manual subclass of Material, are capable of returning a constant
        attenuation coefficient, regardless of the energy of the penetrating
        ray, which is the simplest modelling of a material in this regard """

    def __init__(self, name, mu, uid):
        """ instantiate a material subclass instance """
        try:
            self.name = name
            self.mu   = mu
            self.uid  = Material.uniqueid(self, uid)
            if self.uid == -1:
                raise Exception('{} does not have a new Unique ID (Z) (or has been initialized before).'.format(self.name))
        except Exception as e:
            print(e)
            return

    def __str__(self):
        """ returns a string describing this material """
        return self.name

    def getMu(self, energy):
        """ returns the calculated atenuation coefficient """
        return self.mu



if __name__ == "__main__":
    bigplotmaterial = Material.carbon

    elementals = Material.initElementals()
    biotics    = Material.initBiotics()
    materials  = dict(elementals)
    materials.update(biotics)
    materials[0] = Simplemat('Vacuum',0,0)

    elementals = [key for key in elementals.iterkeys()]
    biotics    = [key for key in biotics.iterkeys()]

    print(elementals)
    print(biotics)

    for key, value in materials.iteritems() :
        print(key, value)

    from matplotlib import pyplot as plt
    i = 0
    for key in elementals+biotics:
        if i % 6 == 0:
            plt.figure()
            plt.suptitle('Linear attenuation coefficients of \n'+\
                 'various materials at standard densities',\
                 fontsize='xx-large')
            i = 0
        i += 1
        title = materials[key].name
        plt.subplot(3,2,i)
        plt.title(title, fontsize='x-large')
        plt.xlabel('E [MeV]', fontsize='large')
        plt.ylabel(' mu [1/cm]', fontsize='large')
        plt.loglog( materials[key].Es, materials[key].mus,\
                    c='r', marker='o', ls='', label='NIST datapoints')
        xs = logspace(-3, 1.2, num=300, base=10)
        ys = [materials[key].getMu(x) for x in xs]
        plt.loglog( xs, ys,  c='b', ls='-', label='Interpolating linear splines')
        plt.legend(loc = 'lower left')
        plt.xticks([10**(-2),10])
        plt.yticks([10**(-2),10])


    plt.figure()
    plt.rc('text', usetex=True)
    #plt.title('Linear attenuation coefficients of Hydrogen',\
    #     fontsize='xx-large')
    title = materials[bigplotmaterial].name
    plt.title(title, fontsize='x-large')
    plt.xlabel('E [MeV]', fontsize='large')
    plt.ylabel(r'\mu [1/cm]', fontsize='large')
    plt.loglog( materials[bigplotmaterial].Es, materials[bigplotmaterial].mus,\
                c='r', marker='o', ls='', label='NIST datapoints')
    xs = logspace(-3, 1.2, num=300, base=10)
    ys = [materials[bigplotmaterial].getMu(x) for x in xs]
    plt.loglog( xs, ys,  c='b', ls='-', label='Interpolating linear splines')
    plt.legend(loc = 'upper right')
    #plt.xlim( (0.001,1) )
    #plt.ylim( (0.00001,0.001))
    plt.show()


# creating plots to visualize comparison of attenuation coefficients
#elementals = Material.initElementals()
#biotics    = Material.initBiotics()
#materials  = dict(elementals)
#materials.update(biotics)
#materials['Vacuum'] = Simplemat('Vacuum',0)
#
#xs = linspace(0.00, 120, 400)
#ys1 = [materials['Blood'].getMu(x/1000) for x in xs]
#ys2 = [materials['Cam'].getMu(x/1000) for x in xs]
#ys3 = [materials['Oak'].getMu(x/1000) for x in xs]
#ys4 = [materials['Bone'].getMu(x/1000) for x in xs]
#ys5 = [materials['Air'].getMu(x/1000) for x in xs]
#ys6 = [materials['Ti'].getMu(x/1000) for x in xs]
#ys7 = [materials['Au'].getMu(x/1000) for x in xs]
#ys8 = [materials['Fe'].getMu(x/1000) for x in xs]
#ys9 = [materials['C'].getMu(x/1000) for x in xs]
#
#plt.figure()
#plt.title('Comparison of attenuation coefficient as function of energy', fontsize='x-large')
#plt.xlabel('E [keV]', fontsize='large')
#plt.ylabel(r'\mu [1/cm]', fontsize='large')
#plt.ylim( (-0.001,2) )
#
#plt.plot(xs,ys1, '--r', label='Blood')
#plt.plot(xs,ys2, '--m', label='Cam')
#plt.plot(xs,ys3, '--g', label='Oak')
#plt.plot(xs,ys4, '--b', label='Bone')
#plt.plot(xs,ys5, '--k', label='Air')
#plt.legend(loc = 'upper right')
#
#
#plt.figure()
#plt.title('Comparison of attenuation coefficient as function of energy', fontsize='x-large')
#plt.xlabel('E [keV]', fontsize='large')
#plt.ylabel(r'\mu [1/cm]', fontsize='large')
#plt.ylim( (-0.001,50e5) )
#plt.xlim( (-0.001,40) )
#
#plt.plot(xs,ys4, '--c', label='Bone')
#plt.plot(xs,ys9, '--k', label='Carbon')
#plt.plot(xs,ys6, '--r', label='Titanium')
#plt.plot(xs,ys8, '--b', label='Iron')
#plt.plot(xs,ys7, '--y', label='Gold')
#plt.legend(loc = 'right')


