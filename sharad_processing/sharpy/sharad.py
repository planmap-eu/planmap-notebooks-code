import logging as log
import os
import numpy as np
from datetime import datetime
import fiona.crs
# log.getLogger().setLevel(log.INFO)

north_pole_crs = fiona.crs.from_string("+proj=stere +lat_0=90 +lat_ts=90 +lon_0=0 +k=1 +x_0=0 +y_0=0 +a=3376200 +b=3376200 +units=m +no_defs")


basepath="http://pds-geosciences.wustl.edu/mro/mro-m-sharad-5-radargram-v1/mrosh_2001"

radargrams =basepath + "/data/rgram/"
geoms =basepath + "/data/geom/"
tiffs =basepath + "/browse/tiff/"
thm = basepath + "/browse/thm/"


geom_names = ["RADARGRAM COLUMN", "TIME", "LATITUDE", "LONGITUDE", "MARS RADIUS", "SPACECRAFT RADIUS", 
                 "RADIAL VELOCITY", "TANGENTIAL VELOCITY", "SZA", "PHASE/1.0E16"]

geom_types = [int, datetime, float, float, float, float, float, float, float, float]
geom_names = [n.replace(" ", "_").replace("/", "_").lower() for n in geom_names]



def create_subpath(code):
    sub = "s_" + code[0:4] + "xx/s_" + code     
    return sub

def get_path_for_img_lbl(code):
    return radargrams + create_subpath(code) + "_rgram.lbl"

def get_path_for_img(code):
    return radargrams + create_subpath(code) + "_rgram.img"

def get_path_for_tiff(code):
    return tiffs + create_subpath(code) + "_tiff.tif"

def get_path_for_tiff_lbl(code):
    return tiffs + create_subpath(code) + "_tiff.lbl"

def get_path_for_jpg_lbl(code):
    return thm + create_subpath(code) + "_thm.lbl"

def get_path_for_jpg(code):
    return thm + create_subpath(code) + "_thm.jpg"

def get_path_for_geom_tab(code):
    return geoms + create_subpath(code) + "_geom.tab"

def get_path_for_geom_lbl(code):
    return geoms + create_subpath(code) + "_geom.lbl"


products = {"RGRAM_LBL": get_path_for_img_lbl, 
            "RGRAM_IMG": get_path_for_img,
            "TIFF": get_path_for_tiff,
            "TIFF_LBL": get_path_for_tiff_lbl,
           "JPG": get_path_for_jpg,
           "JPG_LBL": get_path_for_jpg_lbl,
           "GEOM_TAB": get_path_for_geom_tab,
           "GEOM_LBL": get_path_for_geom_lbl}
 
def download_http_url(url, outfolder="."):
    import requests
    
    if not os.path.exists(outfolder):
        os.makedirs(outfolder, exist_ok=False)
    
    fname = os.path.split(url)[-1]
    fullfilepath = os.path.join(outfolder, fname )
    
    if os.path.exists(fullfilepath):
        log.warning(f"file {fullfilepath} yet exists not repeating")
        return

    r = requests.get(url, allow_redirects=True)
    open(fullfilepath, 'wb').write(r.content)

def download_data_for_sharad_id(items_id_string, folder=".", everything=True, exclude=[]):
    items = np.atleast_1d(items_id_string)
    for i in items:
        for prodname, urlf in products.items():
            if prodname in exclude:
                log.debug(f"Skipping product {prodname} as requested")
                continue
                
            url = urlf(i)
            log.debug(f"downloading {url}")

            download_http_url(url, folder)

#     ftp://pds-geosciences.wustl.edu/mro/mro-m-sharad-5-radargram-v1/mrosh_2001/  browse/thm/s_0407xx/


def find_sharad_radargrams_in_folder(folder):
    import glob
    pattern = folder + "/**/s_*_geom.lbl"
    files = glob.glob(pattern, recursive=True)
    
    log.info(f"found {len(files)} files\n {files}")
    return files

def match_sharad_id(file):
    import regex
    try:
        m = regex.match(".*([0-9]{8}).*", file)
        id = m.group(1)
        return id
    except:
        log.error(f"cannot match {file}")
        return -1
    
    
    

    
def match_sharad_ids(files):
    return  [match_sharad_id(f) for f in files]


from geopandas import GeoDataFrame
from shapely.geometry import Point
import pandas as pd

import fiona

def lbl_to_geom(lbl_file):
    return lbl_file[:-3] + "tab"

def read_geom_lbl(file):
    table = pd.read_csv(file, skiprows=0, names=geom_names)
    return table

def pandas_to_geopandas_points(df, xname="longitude", yname="latitude"):
    geometry = [Point(xy) for xy in zip(df.longitude, df.latitude)]
    crs = fiona.crs.from_string("+proj=longlat +a=3396190 +b=3376200 +no_defs") # MARS 2000
    geo_df = GeoDataFrame(df, crs=crs, geometry=geometry)
    return geo_df
