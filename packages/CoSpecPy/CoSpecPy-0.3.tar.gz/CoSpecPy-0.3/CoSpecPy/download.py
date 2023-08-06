import numpy as np
import scipy
from subprocess import call
import pkg_resources
from glob import glob


class DownloadHandler:
    ''' Class for handling the downloading of spectra given
    a method and various forms of object lists'''

    def __init__(self, download_method, no_of_connections,
                    batch_size, download_folder):

        if download_method != "aria2" and download_method != "wget":
            raise Exception("Valid Download Method is either 'wget' or 'aria2'")
        self.download_method = download_method
        self.no_of_connections = no_of_connections
        self.batch_size = batch_size
        self.download_folder = download_folder

    def download_spectra(self, download_file):
        '''Given spectra list containing correctly formatted URLs, download
        using preferred method given in class initiation'''
        if self.download_method == "aria2":
            call(['aria2c', '-c', '--check-certificate=false',
            '-j', str(self.no_of_connections), '-i', download_file],
            cwd = self.download_folder)

        if self.download_method == "wget":
            call(['wget', '--no-check-certificate', '-c',
            '-i', download_file],
            cwd = self.download_folder)

    def download_example(self):
        ''' Download the example short spectra list in the data directory '''
        DATA_PATH = pkg_resources.resource_filename(__name__, 'data/example_speclist.txt')
        print(DATA_PATH)
        self.download_spectra(DATA_PATH)
        print("Downloaded Succesfully")

    def clear_up(self):
        '''Clear files away from the specified download_folder'''
        files = glob(self.download_folder+'/*.fits')
        call(['rm','-r'] + files)
