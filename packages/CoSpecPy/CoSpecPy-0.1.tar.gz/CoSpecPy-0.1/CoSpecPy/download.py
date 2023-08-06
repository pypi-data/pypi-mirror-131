import numpy as np
import scipy


class DownloadSpectra:
    ''' Class for handling the downloading of spectra given
    a method and various forms of object lists'''
    
    def __init__(self, download_method, no_of_connections, batch_size);
        self.download_method = download_method
        self.no_of_connections = no_of_connections
        self.batch_size = batch_size
