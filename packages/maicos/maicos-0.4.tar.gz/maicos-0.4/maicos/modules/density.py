#!/usr/bin/env python3
# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-
#
# Copyright (c) 2019 Authors and contributors
# (see the file AUTHORS for the full list of names)
#
# Released under the GNU Public Licence, v2 or any higher version
# SPDX-License-Identifier: GPL-2.0-or-later
r"""

The density modules of MAICoS are tools for computing density, 
temperature, and chemical potential profiles from molecular 
simulation trajectory files. Profiles can be extracted either 
in Cartesian or cylindrical coordinate systems. Units for the density 
are the same as GROMACS, i.e. mass, number, charge, and electron. 
See the `gmx density`_ manual for details.

**From the command line**

You can extract a density profile from your molecular dynamics 
trajectories directly from the terminal. For this example, we use 
the ``airwater`` data file of MAICoS. First, go to the directory

.. code-block:: bash

    cd tests/data/airwater/

then type:

.. code-block:: bash

    maicos density_planar -s conf.gro -traj traj.trr

Here ``conf.gro`` and ``traj.trr`` are GROMACS configuration and 
trajectory files, respectively. The density profile appears in 
a ``.dat`` file. You can visualise all the options of the module 
``density_planar`` by typing

.. code-block:: bash

    maicos density_planar -h

**From the Python interpreter**

In order to calculate the density using MAICoS in a Python environment, 
first import MAICoS and MDAnalysis:

.. code-block:: python3

	import MDAnalysis as mda
	import maicos

Then create a MDAnalysis universe:

.. code-block:: python3

	u = mda.Universe('conf.gro', 'traj.trr')
	grpH2O = u.select_atoms('type O or type H')

And run MAICoS' density_planar module:
	
.. code-block:: python3

	dplan = maicos.density_planar(grpH2O)
	dplan.run()   	

Results can be accessed from ``dplan.results``. More details are 
given in the :ref:`tutorial <label_tutorial_density_planar>` below. 

.. _`gmx density`: https://manual.gromacs.org/archive/5.0.7/programs/gmx-density.html

|
"""

import warnings

import numpy as np
from scipy import constants

from .base import MultiGroupAnalysisBase
from ..utils import savetxt, atomgroup_header
from ..decorators import planar_base

from MDAnalysis.exceptions import NoDataError


def mu(rho, temperature, m):
    """Returns the chemical potential calculated from the density: mu = k_B T log(rho. / m)"""
    # kT in KJ/mol
    kT = temperature * constants.Boltzmann * constants.Avogadro / constants.kilo

    results = []

    for srho, mass in zip(np.array(rho).T, m):
        # De Broglie (converted to nm)
        db = np.sqrt(
            constants.h ** 2 / (2 * np.pi * mass * constants.atomic_mass
                                * constants.Boltzmann * temperature)
        ) / constants.nano

        if np.all(srho > 0):
            results.append(kT * np.log(srho * db ** 3))
        elif np.any(srho == 0):
            results.append(np.float64("-inf") * np.ones(srho.shape))
        else:
            results.append(np.float64("nan") * np.ones(srho.shape))
    return np.squeeze(np.array(results).T)


def dmu(rho, drho, temperature):
    """Returns the error of the chemical potential calculated from the density using propagation of uncertainty."""

    kT = temperature * constants.Boltzmann * constants.Avogadro / constants.kilo

    results = []

    for srho, sdrho in zip(np.array(rho).T, np.array(drho).T):
        if np.all(srho > 0):
            results.append(kT * (sdrho / srho))
        else:
            results.append(np.float64("nan") * np.ones(srho.shape))
    return np.squeeze(np.array(results).T)


def weight(selection, dens):
    """Calculates the weights for the histogram depending on the choosen type of density.
        Valid values are `mass`, `number`, `charge` or `temp`."""
    if dens == "mass":
        # amu/nm**3 -> kg/m**3
        return selection.atoms.masses * constants.atomic_mass * 1e27
    elif dens == "number":
        return np.ones(selection.atoms.n_atoms)
    elif dens == "charge":
        return selection.atoms.charges
    elif dens == "temp":
        # ((1 amu * Angstrom^2) / (picoseconds^2)) / Boltzmann constant
        prefac = constants.atomic_mass * 1e4 / constants.Boltzmann
        return ((selection.atoms.velocities ** 2).sum(axis=1) *
                selection.atoms.masses / 2 * prefac)
    else:
        raise ValueError(
            "`{}` not supported. Use `mass`, `number`, `charge` or `temp`".
                format(dens))


@planar_base()
class density_planar(MultiGroupAnalysisBase):
    """Compute partial densities/temperature profiles in the Cartesian systems.

**Tutorial**

.. _label_tutorial_density_planar:

To follow this tutorial, the data test files of MAICoS are needed. 
From a terminal, download MAICoS at a location of your choice:

.. code-block:: bash

    cd mypath
    git clone git@gitlab.com:maicos-devel/maicos.git

In a python environment, import MDAnalysis, MAICoS, PyPlot, and NumPy:

.. code-block:: python3

    import MDAnalysis as mda
    import maicos
    import matplotlib.pyplot as plt
    import numpy as np
    
Define the path to the ``airwater`` data folder of MAICoS:

.. code-block:: python3

    datapath = 'mypath/maicos/tests/data/airwater/'
    
The system consists of a 2D slab with 352 water molecules in vacuum, 
where the two water/vacuum interfaces are normal to the axis :math:`z`:


.. image:: ../images/airwater.png
   :width: 600

Create a universe using MDAnalysis and define a group containing 
the oxygen and the hydrogen atoms of the water molecules:

.. code-block:: python3

    u = mda.Universe(datapath+'conf.gro', datapath+'traj.trr')
    grpH2O = u.select_atoms('type O or type H')

Let us call the ``density_planar`` module:

.. code-block:: python3

    dplan = maicos.density_planar(grpH2O)
    dplan.run()   

Extract the coordinate and the density profile:

.. code-block:: python3

    zcoor = dplan.results['z']
    dens = dplan.results['dens_mean']

By default the binwidth is 0.1 nanometers, the units are kg/m3, 
and the axis is :math:`z`. Plot it using 

.. code-block:: python3

    fig = plt.figure(figsize = (12,6))
    plt.plot(zcoor,dens,linewidth=2)
    plt.xlabel("z coordinate [nanometer]")
    plt.ylabel("density H2O [kg/m3]")
    plt.show()
    
.. image:: ../images/density_planar.png
   :width: 600


They are several options you can play with. To know the full 
list of options, have a look at the ``Inputs`` section below. 
For instance, you can increase the spacial resolution 
by reducing the binwidth:

.. code-block:: python3 

    dplan = maicos.density_planar(grp_oxy, binwidth = 0.05) 
    
**Inputs**
 
:param output (str): Output filename
:param outfreq (int): Default time after which output files are refreshed (1000 ps).
:param dim (int): Dimension for binning (0=X, 1=Y, 2=Z)
:param binwidth (float): binwidth (nanometer)
:param mu (bool): Calculate the chemical potential (sets dens='number')
:param muout (str): Prefix for output filename for chemical potential
:param temperature (float): temperature (K) for chemical potential (Default: 300K)
:param mass (float): Mass (u) for the chemical potential. By default taken from topology.
:param zpos (float): position (nm) at which the chemical potential will be computed. By default average over box.
:param dens (str): Density: mass, number, charge, temperature. (Default: mass)
:param comgroup (str): Perform the binning relative to the center of mass of the selected group.
:param center (bool): Perform the binning relative to the center of the (changing) box.

**Outputs**

:returns (dict): * z: bins
                 * dens_mean: calculated densities
                 * dens_err: density error
                 * mu: chemical potential
                 * dmu: error of chemical potential
                 
|
    """

    def __init__(self,
                 atomgroups,
                 output="density.dat",
                 outfreq=1000,
                 mu=False,
                 muout="muout.dat",
                 temperature=300,
                 mass=None,
                 zpos=None,
                 dens=None,
                 # Planar base arguments are necessary for building CLI
                 dim=2,
                 binwidth=0.1,
                 center=False,
                 comgroup=None,
                 **kwargs):
        super().__init__(atomgroups, **kwargs)
        self.output = output
        self.outfreq = outfreq
        self.mu = mu
        self.muout = muout
        self.temperature = temperature
        self.mass = mass
        self.zpos = zpos
        self.dens = dens

    def _configure_parser(self, parser):
        parser.add_argument('-o', dest='output')
        parser.add_argument('-dout', dest='outfreq')
        parser.add_argument('-mu', dest='mu')
        parser.add_argument('-muo', dest='muout')
        parser.add_argument('-temp', dest='temperature')
        parser.add_argument('-mass', dest='mass')
        parser.add_argument('-zpos', dest='zpos')
        parser.add_argument('-dens', dest='dens')

    def _prepare(self):
        if self.dens is None and self.mu:
            with warnings.catch_warnings():
                warnings.simplefilter('always')
                warnings.warn("Chemical potential calculation requested. "
                              "Using number density.")
            self.dens = "number"
        elif self.dens != "number" and self.mu:
            raise ValueError("Calculation of the chemical potential is only "
                             "possible when number density is selected.")
        elif self.dens is None:
            self.dens = "mass"

        if self.dens not in ["mass", "number", "charge", "temp"]:
            raise ValueError(
                "Invalid choice for dens: '{}' (choose from 'mass', "
                "'number', 'charge', 'temp')".format(self.dens))
        if self._verbose:
            if self.dens == 'temp':
                print('Computing temperature profile along {}-axes.'.format(
                    'XYZ'[self.dim]))
            else:
                print('Computing {} density profile along {}-axes.'.format(
                    self.dens, 'XYZ'[self.dim]))

        self.density_mean = np.zeros((self.n_bins, self.n_atomgroups))
        self.density_mean_sq = np.zeros((self.n_bins, self.n_atomgroups))

        if self.mu:
            if not self.mass:
                try:
                    self.atomgroups[0].universe.atoms.masses
                except NoDataError:
                    raise ValueError(
                        "Calculation of the chemical potential is only possible"
                        " when masses are present in the topology or masses are"
                        "supplied by the user.")
                get_mass_from_topol = True
                self.mass = np.array([])
            else:
                if len([self.mass]) == 1:
                    self.mass = np.array([self.mass])
                else:
                    self.mass = np.array(self.mass)
                get_mass_from_topol = False

            self.n_res = np.array([])
            self.n_atoms = np.array([])

            for ag in self.atomgroups:
                if not len(ag.atoms) == len(ag.residues.atoms):
                    with warnings.catch_warnings():
                        warnings.simplefilter('always')
                        warnings.warn("Selections contains incomplete residues."
                                      "MAICoS uses the total mass of the "
                                      "residues to calculate the chemical "
                                      "potential. Your results will be "
                                      "incorrect! You can supply your own "
                                      "masses with the -mass flag.")

                ag_res = ag.residues
                mass = []
                n_atoms = 0
                n_res = 0
                while len(ag_res.atoms):
                    n_res += 1
                    resgroup = ag_res - ag_res
                    n_atoms += len(ag_res.residues[0].atoms)

                    for res in ag_res.residues:
                        if np.all(res.atoms.types
                                  == ag_res.residues[0].atoms.types):
                            resgroup = resgroup + res
                    ag_res = ag_res - resgroup
                    if get_mass_from_topol:
                        mass.append(resgroup.total_mass() / resgroup.n_residues)
                if not n_res == n_atoms and n_res > 1:
                    raise NotImplementedError(
                        "Selection contains multiple types of residues and at "
                        "least one them is a molecule. Molecules are not "
                        "supported when selecting multiple residues."
                    )
                self.n_res = np.append(self.n_res, n_res)
                self.n_atoms = np.append(self.n_atoms, n_atoms)
                if get_mass_from_topol:
                    self.mass = np.append(self.mass, np.sum(mass))

    def _single_frame(self):
        curV = self._ts.volume / 1000

        for index, selection in enumerate(self.atomgroups):
            bins = self.get_bins(selection.atoms.positions)
            density_ts = np.histogram(bins,
                                      bins=np.arange(self.n_bins + 1),
                                      weights=weight(selection, self.dens))[0]

            if self.dens == 'temp':
                bincount = np.bincount(bins, minlength=self.n_bins)
                self.density_mean[:, index] += density_ts / bincount
                self.density_mean_sq[:, index] += (density_ts / bincount) ** 2
            else:
                self.density_mean[:, index] += density_ts / curV * self.n_bins
                self.density_mean_sq[:, index] += (density_ts / curV *
                                                   self.n_bins) ** 2

        if self._save and self._frame_index % self.outfreq == 0 and self._frame_index > 0:
            self._calculate_results()
            self._save_results()

    def _calculate_results(self):
        self._index = self._frame_index + 1

        self.results["dens_mean"] = self.density_mean / self._index
        self.results["dens_mean_sq"] = self.density_mean_sq / self._index

        self.results["dens_std"] = np.nan_to_num(
            np.sqrt(self.results["dens_mean_sq"] -
                    self.results["dens_mean"] ** 2))
        self.results["dens_err"] = self.results["dens_std"] / \
                                   np.sqrt(self._index)

        # chemical potential
        if self.mu:
            if self.zpos is not None:
                this = (np.rint(
                    (self.zpos + self.binwidth / 2) / self.binwidth)
                        % self.n_bins).astype(int)
                if self.center:
                    this += np.rint(self.n_bins / 2).astype(int)
                self.results["mu"] = mu(self.results["dens_mean"][this]
                                        / self.n_atoms,
                                        self.temperature, self.mass)
                self.results["dmu"] = dmu(self.results["dens_mean"][this]
                                          / self.n_atoms,
                                          self.results["dens_err"][this]
                                          / self.n_atoms, self.temperature)
            else:
                self.results["mu"] = np.mean(
                    mu(self.results["dens_mean"] / self.n_atoms,
                       self.temperature,
                       self.mass), axis=0)
                self.results["dmu"] = np.mean(
                    dmu(self.results["dens_mean"] / self.n_atoms,
                        self.results["dens_err"],
                        self.temperature), axis=0)

    def _save_results(self):
        # write header
        if self.dens == "mass":
            units = "kg m^(-3)"
        elif self.dens == "number":
            units = "nm^(-3)"
        elif self.dens == "charge":
            units = "e nm^(-3)"
        elif self.dens == "temp":
            units = "K"

        if self.dens == 'temp':
            columns = "temperature profile [{}]".format(units)
        else:
            columns = "{} density profile [{}]".format(self.dens, units)
        columns += "\nstatistics over {:.1f} picoseconds \npositions [nm]".format(
            self._index * self._universe.trajectory.dt)
        try:
            for group in self.atomgroups:
                columns += "\t" + atomgroup_header(group)
            for group in self.atomgroups:
                columns += "\t" + atomgroup_header(group) + " error"
        except AttributeError:
            with warnings.catch_warnings():
                warnings.simplefilter('always')
                warnings.warn("AtomGroup does not contain resnames."
                              " Not writing residues information to output.")

        # save density profile
        savetxt(self.output,
                np.hstack(
                    (self.results["z"][:, np.newaxis],
                     self.results["dens_mean"], self.results["dens_err"])),
                header=columns)

        if self.mu:
            if self.zpos is not None:
                columns = "Chemical potential calculated at z = {} nm.".format(
                    self.zpos)
            else:
                columns = "Chemical potential averaged over the whole system."
            columns += "\nstatistics over {:.1f} picoseconds \n".format(
                self._index * self._universe.trajectory.dt)
            try:
                for group in self.atomgroups:
                    columns += atomgroup_header(group) + " μ [kJ/mol]" + "\t"
                for group in self.atomgroups:
                    columns += atomgroup_header(group) + " μ error [kJ/mol]" \
                               + "\t"
            except AttributeError:
                with warnings.catch_warnings():
                    warnings.simplefilter('always')
                    warnings.warn("AtomGroup does not contain resnames."
                                  " Not writing residues information to "
                                  "output.")
            # save chemical potential
            savetxt(self.muout,
                    np.hstack((self.results["mu"], self.results["dmu"]))[None],
                    header=columns)


class density_cylinder(MultiGroupAnalysisBase):
    """Compute partial densities across a cylinder.

**Inputs**
 
:param output (str): Output filename
:param outfreq (int): Default time after which output files are refreshed (1000 ps).
:param dim (int): Dimension for binning (0=X, 1=Y, 2=Z)
:param center (str): Perform the binning relative to the center of this selection string of teh first AtomGroup.
                     If None center of box is used.
:param radius (float): Radius of the cylinder (nm). If None smallest box extension is taken.
:param binwidth (float): binwidth (nanometer)
:param length (float): Length of the cylinder (nm). If None length of box in the binning dimension is taken.
:param dens (str): Density: mass, number, charge, temp

**Outputs**

:returns (dict): * z: bins
                 * dens_mean: calculated densities
                 * dens_err: density error

**Tutorial**

To follow this tutorial, the data test files of MAICoS are needed. 
From a terminal, download MAICoS at a location of your choice:

.. code-block:: bash

    cd mypath
    git clone git@gitlab.com:maicos-devel/maicos.git

In a python environment, import MDAnalysis, MAICoS, and PyPlot:

.. code-block:: python3

    import MDAnalysis as mda
    import maicos
    import matplotlib.pyplot as plt	    

Define the path to the ``cntwater`` data folder of MAICoS:

.. code-block:: python3

    datapath = 'mypath/maicos/tests/data/cntwater/'
	    
The system consists of a carbon nanotube (CNT) with axis in the 
:math:`z`: direction, a radius of about 2 nm, a of length 2.2 nm, 
and filled with 810 water molecules.

.. image:: ../images/cntwater.png
    :width: 400

Create a universe using MDAnalysis and define two groups, 
one containing the water molecules, one containing the
carbon atoms:

.. code-block:: python3

    u = mda.Universe(datapath + 'lammps.data', datapath + 'traj.xtc')
    grpH2O = u.select_atoms('type 1 or type 2')
    grpCNT = u.select_atoms('type 3')

Call the ``density_cylinder`` module for the two groups:

.. code-block:: python3

    dcylH2O = maicos.density_cylinder(grpH2O, center='all', binwidth = 0.01)
    dcylH2O.run()   
    dcylCNT = maicos.density_cylinder(grpCNT, center='all', binwidth = 0.01)
    dcylCNT.run() 

With the keyword ``center='all'``, the center of mass of all the atoms 
of the group is used as the center of the density profile. 
If not specified, the center of the box is used. 

Finally, extract the coordinates and the density profiles:

.. code-block:: python3

    rcoor = dcylH2O.results['r']
    densH2O = dcylH2O.results['dens_mean']
    densCNT = dcylCNT.results['dens_mean']
    
Plot it using PyPlot: 

.. code-block:: python3

    fig = plt.figure(figsize = (12,6))
    plt.plot(rcoor,densH2O,linewidth=2)
    plt.plot(rcoor,densCNT,linewidth=2)
    plt.xlabel("r coordinate [nanometer]")
    plt.ylabel("density [kg/m3]")
    plt.show()
	    
.. image:: ../images/density_cylinder.png
    :width: 600    
   
|
    """

    def __init__(self,
                 atomgroups,
                 output="density_cylinder.dat",
                 outfreq=1000,
                 dim=2,
                 center=None,
                 radius=None,
                 binwidth=0.1,
                 length=None,
                 dens="mass",
                 **kwargs):
        super().__init__(atomgroups, **kwargs)
        self.output = output
        self.outfreq = outfreq
        self.dim = dim
        self.binwidth = binwidth
        self.center = center
        self.radius = radius
        self.length = length
        self.dens = dens

    def _configure_parser(self, parser):
        parser.add_argument('-o', dest='output')
        parser.add_argument('-dout', dest='outfreq')
        parser.add_argument('-d', dest='dim')
        parser.add_argument('-center', dest='center')
        parser.add_argument('-r', dest='radius')
        parser.add_argument('-dr', dest='binwidth')
        parser.add_argument('-l', dest='length')
        parser.add_argument('-dens', dest='dens')

    def _prepare(self):

        if self.dens not in ["mass", "number", "charge", "temp"]:
            raise ValueError(
                "Invalid choice for dens: '{}' (choose from 'mass', "
                "'number', 'charge', 'temp')".format(self.dens))

        if self._verbose:
            if self.dens == 'temp':
                print('Computing temperature profile along {}-axes.'.format(
                    'XYZ'[self.dim]))
            else:
                print(
                    'Computing radial {} density profile along {}-axes.'.format(
                        self.dens, 'XYZ'[self.dim]))

        self.odims = np.roll(np.arange(3), -self.dim)[1:]

        if self.center is None:
            if self._verbose:
                print("No center given --> Take from box dimensions.")
            self.centersel = None
            center = self.atomgroups[0].dimensions[:3] / 2
        else:
            self.centersel = self.atomgroups[0].select_atoms(self.center)
            if len(self.centersel) == 0:
                raise RuntimeError("No atoms found in center selection. "
                                   "Please adjust selection!")
            center = self.centersel.center_of_mass()

        if self._verbose:
            print("Initial center at {}={:.3f} nm and {}={:.3f} nm.".format(
                'XYZ'[self.odims[0]], center[self.odims[0]] / 10,
                'XYZ'[self.odims[1]], center[self.odims[1]] / 10))

        if self.radius is None:
            self.radius = self.atomgroups[0].dimensions[self.odims].min() / 2
            if self._verbose:
                print(
                    "No radius given --> Take smallest box extension (r={:.2f} nm)."
                        .format(self.radius / 10))
        else:
            self.radius /= 10

        if self.length is None:
            self.length = self.atomgroups[0].dimensions[self.dim]
            if self._verbose:
                print("No length given --> Take length in {}.".format(
                    'XYZ'[self.dim]))
        else:
            self.length /= 10

        self.nbins = int(np.ceil(self.radius / 10 / self.binwidth))

        self.density_mean = np.zeros((self.nbins, self.n_atomgroups))
        self.density_mean_sq = np.zeros((self.nbins, self.n_atomgroups))

        self._dr = np.ones(self.nbins) * self.radius / self.nbins
        self._r_bins = np.arange(self.nbins) * self._dr + self._dr
        self._delta_r_sq = self._r_bins ** 2 - \
                           np.insert(self._r_bins, 0, 0)[0:-1] ** 2  # r_o^2 - r_i^2

        if self._verbose:
            print("\n")
            print('Using', self.nbins, 'bins.')

    def _single_frame(self):
        # calculater center of cylinder.
        if self.center is None:
            center = self.atomgroups[0].dimensions[:3] / 2
        else:
            center = self.centersel.center_of_mass()

        for index, selection in enumerate(self.atomgroups):

            # select cylinder of the given length and radius
            cut = selection.atoms[np.where(
                np.absolute(selection.atoms.positions[:, self.dim] -
                            center[self.dim]) < self.length / 2)[0]]
            cylinder = cut.atoms[np.where(
                np.linalg.norm((cut.atoms.positions[:, self.odims] -
                                center[self.odims]),
                               axis=1) < self.radius)[0]]

            radial_positions = np.linalg.norm(
                (cylinder.atoms.positions[:, self.odims] - center[self.odims]),
                axis=1)
            bins = np.digitize(radial_positions, self._r_bins)
            density_ts = np.histogram(bins,
                                      bins=np.arange(self.nbins + 1),
                                      weights=weight(cylinder, self.dens))[0]

            if self.dens == 'temp':
                bincount = np.bincount(bins, minlength=self.nbins)
                self.density_mean[:, index] += density_ts / bincount
                self.density_mean_sq[:, index] += (density_ts / bincount) ** 2
            else:
                self.density_mean[:, index] += density_ts * 1000 / (
                        np.pi * self._delta_r_sq * self.length)
                self.density_mean_sq[:, index] += (
                                                          density_ts * 1000 /
                                                          (np.pi * self._delta_r_sq * self.length)) ** 2

        if self._save and self._frame_index % self.outfreq == 0 and self._frame_index > 0:
            self._calculate_results()
            self._save_results()

    def _calculate_results(self):
        self._index = self._frame_index + 1

        self.results["r"] = (np.copy(self._r_bins) - self._dr / 2) / 10
        self.results["dens_mean"] = self.density_mean / self._index
        self.results["dens_mean_sq"] = self.density_mean_sq / self._index

        self.results["dens_std"] = np.nan_to_num(
            np.sqrt(self.results["dens_mean_sq"] -
                    self.results["dens_mean"] ** 2))
        self.results["dens_err"] = self.results["dens_std"] / np.sqrt(
            self._index)

    def _save_results(self):
        # write header
        if self.dens == "mass":
            units = "kg m^(-3)"
        elif self.dens == "number":
            units = "nm^(-3)"
        elif self.dens == "charge":
            units = "e nm^(-3)"
        elif self.dens == "temp":
            units = "K"

        if self.dens == 'temp':
            columns = "temperature profile [{}]".format(units)
        else:
            columns = "{} density profile [{}]".format(self.dens, units)
        columns += "\nstatistics over {:.1f} picoseconds \npositions [nm]".format(
            self._index * self._universe.trajectory.dt)
        for group in self.atomgroups:
            columns += "\t" + atomgroup_header(group)
        for group in self.atomgroups:
            columns += "\t" + atomgroup_header(group) + " error"

        # save density profile
        savetxt(self.output,
                np.hstack(
                    ((self.results["r"][:, np.newaxis]),
                     self.results["dens_mean"], self.results["dens_err"])),
                header=columns)
