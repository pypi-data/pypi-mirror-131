import numpy as np
from glob import glob
import scipy.interpolate as interp
from astropy.cosmology import Planck15
from astropy.io import fits


def extract_spectra(file):
    ''' Function to extract spectra from SDSS fits format'''
    data = fits.open(file)

    spec_data = data[1].data
    info = data[2].data

    z = info['Z']

    flux = spec_data['flux']
    loglam = spec_data['loglam']

    lam = 10**loglam
    restlam = lam/(1+z)
    data.close()

    return z, flux, restlam

def composite_run(file_list, comp_wavs,
                        norm_fluxes, normal_wav_low, normal_wav_high):
    ''' One composite run through a file_list.
            Returns normalised fluxes for all spectra '''
    fluxes = []
    avg = []

    for file in file_list:
        z, flux, restlam = extract_spectra(file)



        min_wav = np.min(restlam)
        max_wav = np.max(restlam)

        flux_interp = interp.interp1d(restlam, flux, bounds_error = False)


        min_overlap = np.argmin(np.abs(comp_wavs - min_wav))
        max_overlap = np.argmin(np.abs(comp_wavs- max_wav))

        flux_array = np.empty(len(comp_wavs))

        flux_array[:] = np.nan

        flux_array[min_overlap:max_overlap] = flux_interp(np.linspace(comp_wavs[min_overlap], comp_wavs[max_overlap], max_overlap-min_overlap))

        #Here we average over a wavelength range to scale the composite spectra


        arg_normal_low = np.argmin(np.abs(comp_wavs-normal_wav_low))
        arg_normal_high = np.argmin(np.abs(comp_wavs-normal_wav_high))

        scaling_factor = np.mean(flux_array[arg_normal_low:arg_normal_high])
        avg.append(scaling_factor)
        #print(flux_array[arg_normal])

        normalised_array = flux_array/scaling_factor

        #print(normalised_array)

        norm_fluxes.append(normalised_array)

    print("Median Correction: %.4g"%np.nanmean(avg))


def write_output(filename, norm_fluxes):
    '''Save an array of normalised fluxes to a .npy binary'''
    np.save(filename, norm_fluxes)
    print('Saving to output: ' + filename)


def jacknife_test(fluxes, median_flux, std_flux):

    ''' To implement, require to be within uncertainties throughout'''

    overall_median = median_flux
    overall_std = std_flux
    sum_std = np.nansum(overall_std)
    indexes = []
    for i in range(len(fluxes)):
        new_fluxes = fluxes[:i-1:]
        median_flux = np.nanmedian(new_fluxes, axis = 0)
        residual = np.abs(median_flux - overall_median)
        sum_residual = np.nansum(residual)
        #print('Sum_std: %s'%sum_std)
        #print('Sum_residual: %s'%sum_residual)
        if sum_residual<sum_std:
            indexes.append(i)

    return indexes



def boostrap_fluxes(fluxes, samples = 100):
    medians = []


    for sample in range(samples):
        #Select 60% of the sample for each subset
        tmp_flux_inds = np.random.choice(range(len(fluxes)), int(len(fluxes)*0.6), replace=True)
        medians.append(np.nanmedian(fluxes[tmp_flux_inds], axis = 0))

    median_flux = np.nanmedian(medians, axis = 0)
    std_flux = np.nanstd(medians, axis = 0)/np.sqrt(100/60) # Determine uncertainty

    index_knife = jacknife_test(fluxes, median_flux, std_flux)
    if len(index_knife)>0:
        medians = []
        fluxes = fluxes[index_knife]
        for sample in range(samples):
            #Select 60% of the sample for each subset
            tmp_flux_inds = np.random.choice(range(len(fluxes)), int(len(fluxes)*0.6), replace=True)
            medians.append(np.nanmedian(fluxes[tmp_flux_inds], axis = 0))
        median_flux = np.nanmedian(medians, axis = 0)
        std_flux = np.nanstd(medians, axis = 0)/np.sqrt(100/60) # Determine uncertainty


    return median_flux, std_flux
