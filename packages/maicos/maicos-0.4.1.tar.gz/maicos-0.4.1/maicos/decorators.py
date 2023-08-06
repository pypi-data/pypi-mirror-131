#!/usr/bin/env python3
# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-
#
# Copyright (c) 2020 Authors and contributors
# (see the file AUTHORS for the full list of names)
#
# Released under the GNU Public Licence, v2 or any higher version
# SPDX-License-Identifier: GPL-2.0-or-later

import functools
import warnings

import numpy as np

from .arg_completion import _append_to_doc


def planar_base():
    """Class Decorator to provide options and attributes for analysis in planar
    cofinenement. Decorator will add the options `dim`, `bindwidth`, 
    `comgroup`, `center` to the AnalysisClass.
    `dim` controls the direction of binning and `bindwidth` the 
    bindwidth in nanometers. With `comgroup` the binning is performed relative 
    to the center of mass of the selected group. With `center` the 
    binning is preformed relative to the center of the (changing) box.

    Furthermore the item "z" is added automatically to the classes 
    results dictionary.
    """
    def inner(original_class):
        # Make copy of original functions, so we can call them
        # without recursion problems.
        orig_init = original_class.__init__
        orig_configure_parser = original_class._configure_parser
        orig_prepare = original_class._prepare
        orig_single_frame = original_class._single_frame
        orig_calculate_results = original_class._calculate_results

        @functools.wraps(original_class.__init__)
        def __init__(self,
                     atomgroups,
                     *args,
                     dim=2,
                     binwidth=0.1,
                     center=False,
                     comgroup=None,
                     **kwargs):
            # Call the original __init__ first to append arguments.
            orig_init(self, atomgroups, *args, **kwargs)
            self.dim = dim
            self.binwidth = binwidth
            self.center = center
            self.comgroup = comgroup

            # TODO: Try to manipulate signature to get rid of standard 
            # arguments in decorated planar classes.
            # Or find a way to extract default arguments, while building CLI...

        def _configure_parser(self, parser):
            # Call the original _configure_parser first to append arguments.
            orig_configure_parser(self, parser)
            parser.add_argument('-d', dest='dim')
            parser.add_argument('-dz', dest='binwidth')
            parser.add_argument('-com', dest='comgroup')
            parser.add_argument('-center', dest='center')

        def _prepare(self):
            if self.dim not in [0, 1, 2]:
                raise ValueError("Dimension can only be 0=X or 1=Y or 2=Z.")

            # Workaround since currently not alle module have option 
            # with zmax and zmin
            if not hasattr(self, 'zmax'):
                self.zmax = -1

            if self.zmax == -1:
                zmax = self._universe.dimensions[self.dim]
            else:
                self.zmax *= 10
                zmax = self.zmax

            if not hasattr(self, 'zmin'):
                self.zmin = 0
            self.zmin = 10 * self.zmin

            self.n_bins = int(np.ceil((zmax - self.zmin) / 10 / self.binwidth))

            if self._verbose:
                print('Using', self.n_bins, 'bins.')

            if self.comgroup is not None:
                self.comsel = self._universe.select_atoms(self.comgroup)
                if self._verbose:
                    print("Performing the binning relative to the "
                          "center of mass of '{}' containing {} atoms.".format(
                          self.comgroup, self.comsel.n_atoms))
                if self.comsel.n_atoms == 0:
                    raise ValueError(
                        "`{}` does not contain any atoms. Please adjust "
                        "'com' selection.".format(self.comgroup))
            if self.comgroup is not None:
                self.center = True  # always center when COM

            self.Lz = 0
            orig_prepare(self)

        def get_bins(self, positions, dim=None):
            """"Calculates bins based on given positions. dim denotes 
            the dimension for calculating bins. If `None` the default 
            dim is taken.
            
            Attributes
            ----------
            positions : numpy.ndarray
                3 dimensional positions
            dim : int
                dimesion for binning (x=0, y=1, z=2)"""
            dim = self.dim if dim is None else dim
            dz = self._ts.dimensions[dim] / self.n_bins
            bins = np.rint(positions[:, dim] / dz) 
            bins %= self.n_bins
            return bins.astype(int)

        def _single_frame(self, *args, **kwargs):
            self.Lz += self._ts.dimensions[self.dim]
            # Center of mass calculation with generalization to periodic systems
            # see Bai, Linge; Breen, David (2008). "Calculating Center of Mass in an
            # Unbounded 2D Environment". Journal of Graphics, GPU, and Game Tools. 13
            # (4): 53–60. doi:10.1080/2151237X.2008.10129266,
            # https://en.wikipedia.org/wiki/Center_of_mass
            # Systems_with_periodic_boundary_conditions

            if self.comgroup is not None:
                Theta = self.comsel.positions[:,
                                              self.dim] / self._ts.dimensions[
                                                  self.dim] * 2 * np.pi
                Xi = (np.cos(Theta) *
                      self.comsel.masses).sum() / self.comsel.masses.sum()
                Zeta = (np.sin(Theta) *
                        self.comsel.masses).sum() / self.comsel.masses.sum()
                ThetaCOM = np.arctan2(-Zeta, -Xi) + np.pi
                comshift = self._ts.dimensions[self.dim] * (0.5 - ThetaCOM / (2 * np.pi))

                # Check if SingleGroupAnalysis
                if hasattr(self, 'atomgroup'):
                    groups = [self.atomgroup]
                else:
                    groups = self.atomgroups
                for group in groups:
                    group.atoms.positions += comshift

            # Call the original _single_frame
            orig_single_frame(self, *args, **kwargs)

        def _calculate_results(self):
            self._index = self._frame_index + 1

            if self.zmax == -1:
                zmax = self.Lz / self._index
            else:
                zmax = self.zmax

            dz = (zmax - self.zmin) / self.n_bins

            self.results["z"] = np.linspace(
                self.zmin+dz/2, zmax-dz/2, self.n_bins,
                endpoint=False)

            if self.center:
                self.results["z"] -= self.zmin + (zmax - self.zmin) / 2

            self.results["z"] /= 10
            orig_calculate_results(self)

        extra_params = [
        {
            "name": "dim",
            "type": int,
            "doc": "Dimension for binning (0=X, 1=Y, 2=Z)\n"
        }, {
            "name": "binwidth",
            "type": float,
            "doc": "binwidth (nanometer)\n"
        }, {
            "name": "comgroup",
            "type": str,
            "doc": "Perform the binning relative to the "
                   "center of mass of the selected group."
                   "With `comgroup` the `center` option is also used.\n"
        }, {
            "name": "center",
            "type": bool,
            "doc": "Perform the binning relative to the center of the "
                   "(changing) box.\n"
        }]

        original_class.__doc__ = _append_to_doc(original_class.__doc__,
                                                params=extra_params)

        # Set the class functions to the new ones
        original_class.__init__ = __init__
        original_class._configure_parser = _configure_parser
        original_class._prepare = _prepare
        original_class.get_bins = get_bins
        original_class._single_frame = _single_frame
        original_class._calculate_results = _calculate_results

        return original_class

    return inner


def charge_neutral(filter):
    """Class Decorator to raise an Error/Warning when AtomGroup in an AnalysisBase class
    is not charge neutral. The behaviour of the warning can be controlled
    with the filter attribute. If the AtomGroup's corresponding universe is non-neutral
    an ValueError is raised.

    :param filter (str): Filter type to control warning filter
                         Common values are: "error" or "default"
                         See `warnings.simplefilter` for more options.
    """
    def inner(original_class):
        def charge_check(function):
            @functools.wraps(function)
            def wrapped(self):
                # Check if SingleGroupAnalysis
                if hasattr(self, 'atomgroup'):
                    groups = [self.atomgroup]
                else:
                    groups = self.atomgroups
                for group in groups:
                    if not np.allclose(
                            group.total_charge(compound='fragments'), 0,
                            atol=1E-5):
                        with warnings.catch_warnings():
                            warnings.simplefilter(filter)
                            warnings.warn(
                                "At least one AtomGroup has free charges. "
                                "Analysis for systems with free charges could lead "
                                "to severe artifacts!")

                    if not np.allclose(group.universe.atoms.total_charge(), 0,
                                       atol=1E-5):
                        raise ValueError(
                            "Analysis for non-neutral systems is not supported."
                        )
                return function(self)

            return wrapped

        original_class._prepare = charge_check(original_class._prepare)

        return original_class

    return inner
