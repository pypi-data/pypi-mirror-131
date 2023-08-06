# CoSpecPy - SDSS Composites Made Easy

This is a package written for the purpose of creating composite spectra from SDSS data releases.

Future releases will contain additional features for plotting and uncertainty information. Connections to astropy Tables and queries are also a possibility.

## Install Instructions

Install using `pip` available through:

`pip install CoSpecPy`

Or alternatively you can clone this GitHub repository, navigate to the directory you have just cloned and run:

`python setup.py install`

## Quick Start

The only feature currently implemented (Day 1) is the `DownloadHandler` and the basics of the main `Composite` class. Make sure that either `wget` or `aria2` is installed on your machine.

For a quick example you can use

```python
from CoSpecPy import DownloadHandler, Composite # Import the Handler

output_dir = "/path/to/output"

example_handler = DownloadHandler(download_method = "wget", #Download method (aria2 or wget)
no_of_connections = 1, batch_size="10", #Connections only apply to aria2, batches not implemented
 download_folder=output_dir) # output folder

#Example download with wget
example_handler.download_example()

#This will download the 50 example spectra in CoSpecPy/data/example_speclist.txt to your chosen output

example_composite = Composite(name = "example_composite") #Creation of Composite Class
example_composite.add_wavelength_grid(w_min = 1000, w_max = 3000, steps = 2500) #Add the desired wavelength grid in Angstrom
example_composite.add_normalisation(norm_low = 2575, norm_high = 2625) #Add desired normalisation range in Angstrom
example_composite.composite_from_downloads(output_dir) # Will create the composite
example_composite.plot_composite() # Plots the composite stored in the composite class with bootstrapped uncertainties

# Optional
example_composite.save_composite("example.npy") #Write composite to binary .npy file
```

Output should look something like this

![./example.png](./example.png)

## Download Dependencies

The `DownloadHandler` requires use of either `wget` or `aria2` to download from the SDSS servers.

`wget` is GNU Wget is a free software package for retrieving files using HTTP, HTTPS, FTP and FTPS. Information and documentation can be found here [https://www.gnu.org/software/wget/](https://www.gnu.org/software/wget/). For a quick Debian/Ubuntu install try:

`sudo apt-get install wget`

`aria2` is a lightweight multi-protocol & multi-source command-line download utility. Information and documentation can be found here [https://aria2.github.io/](https://aria2.github.io/). For a quick Debian/Ubuntu install try:

`sudo apt-get install -y aria2`

## Features Implemented

Download of spectra list using either `aria2` or `wget`. `aria2` allows for easy opening of multiple connections for a much faster download.

Example included with `DownloadHandler.download_example()`

## Future Features

- Batch-split downloads given spectra list
- Spectral composite making from downloads - Options for wavelength grid, normalisation range, uncertainty estimation, plotting
- Helper functions to go from an `astropy.Table` through to composite making
- Possible inclusion of SDSS querying to create the fetch information for speclist
- Long-term, add external features such as redenning estimation  
