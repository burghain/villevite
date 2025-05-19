import subprocess
import os


'''
This class is intended to download and later remove data of only one map excerpt.

Use a separate instance for each map excerpt.
'''
class OSMDownloader():

    '''
    coords.. 4-tuple (minlon, minlat, maxlon, maxlat)
    filename.. Name of file to download to in the Assets folder
    '''
    def __init__(self, coords, filename):
        self.coords = coords
        self.filepath = f'{os.getcwd()}/villevite/Assets/{filename}'

    '''
    Downloads a map excerpt to the specified file in the Assets folder
    '''
    def download_to_file(self):
        subprocess.run(['wget',
                       '-O',
                       self.filepath,
                       f'https://www.openstreetmap.org/api/0.6/map?bbox={self.coords[0]},{self.coords[1]},{self.coords[2]},{self.coords[3]}'])
    
    '''
    Delete the downloaded data
    '''
    def clear(self):
        os.remove(self.filepath)