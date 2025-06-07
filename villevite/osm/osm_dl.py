import subprocess
import os
import osmium


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
        self.dir = f'{os.getcwd()}/villevite/Assets/'
        self.filepath_xml = f'{self.dir}{filename}.osm'
        self.filepath_pbf = f'{self.dir}{filename}.pbf'

    '''
    Downloads a map excerpt to the specified file in the Assets folder
    '''
    def download_to_file(self):
        subprocess.run(['wget',
                       '-O',
                       self.filepath_xml,
                       f'https://www.openstreetmap.org/api/0.6/map?bbox={self.coords[0]},{self.coords[1]},{self.coords[2]},{self.coords[3]}'])
        
        with osmium.SimpleWriter(self.filepath_pbf) as writer:
            for o in osmium.FileProcessor(self.filepath_xml):
                writer.add(o)

    
    '''
    Delete the downloaded data
    '''
    def clear(self):
        os.remove(self.filepath_xml)
        os.remove(self.filepath_pbf)