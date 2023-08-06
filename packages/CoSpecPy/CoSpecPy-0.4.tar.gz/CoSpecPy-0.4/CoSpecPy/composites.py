from .download import DownloadHandler
from .composite_helpers import *

import scipy.interpolate as interp
import numpy as np
from astropy.io import fits


from glob import glob

import pkg_resources

class Composite:
    '''Composite Class to handle creation of composites'''

    def __init__(self, name):
        self.name = name
        self.fluxes = []

    def add_wavelength_grid(self, w_min, w_max, steps):
        ''' Add the common wavelength grid which we will place
            spectra in '''
        self.w_min = w_min
        self.w_max = w_max
        self.wavelength_grid = np.linspace(w_min, w_max, steps)

    def add_normalisation(self, norm_low, norm_high):
        '''Add upper and lower normalisation values'''
        self.norm_low = norm_low
        self.norm_high = norm_high


    def composite_from_downloads(self, download_folder):
        '''Create composite from a directory of downloaded spectra'''

        file_list = glob(download_folder+"/*.fits")
        output_fluxes = [] #Initalise empty list for fluxes

        composite_run(file_list, self.wavelength_grid,
                        output_fluxes, self.norm_low, self.norm_high)
        self.fluxes = np.array(output_fluxes)


    def save_composite(self, filename):
        '''Save current set of fluxes to .npy file'''
        write_output(filename, self.fluxes)




    def plot_composite(self):
        '''Simple plot of the current composite'''

        import matplotlib.pyplot as plt

        median_flux, std_flux = boostrap_fluxes(self.fluxes, 500)
        plot_flux = median_flux*3e8/self.wavelength_grid
        difference = std_flux*3e8/self.wavelength_grid


        plt.figure(figsize = (12, 7))
        plt.plot(self.wavelength_grid, plot_flux, linewidth = 0.5)
        plt.fill_between(self.wavelength_grid, plot_flux-difference,
                            plot_flux+difference, alpha = 0.5)
        plt.xlabel(r"$\lambda$ [Å]", fontsize = 'xx-large')
        plt.ylabel(r"$F \nu$", fontsize = 'xx-large')
        plt.yscale('log')
        plt.xlim(self.w_min, self.w_max)
        plt.title("Composite: %s"%self.name)

        plt.show()

    def example_from_downloads(self, download_folder):
        '''Full example run using the already downloaded list'''
        self.add_wavelength_grid(1000, 3000, 2500)
        self.add_normalisation(2575, 2625)


        self.composite_from_downloads(download_folder)


        self.plot_composite()
