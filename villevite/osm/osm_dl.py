import subprocess
import os

class OSMDownloader():

    '''
    Downloads a map excerpt to a specified file in the Assets folder

    coords.. 4-tuple (minlon, minlat, maxlon, maxlat)
    filename.. Name of file to download to
    '''
    def download_to_file(self, coords, filename):
        subprocess.run(['wget',
                       '-O',
                       f'{os.getcwd()}/villevite/Assets/{filename}',
                       f'https://www.openstreetmap.org/api/0.6/map?bbox={coords[0]},{coords[1]},{coords[2]},{coords[3]}'])