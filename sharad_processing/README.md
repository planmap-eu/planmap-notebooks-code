# sharpy - preliminary release
Sharad data search, download and conversion in just a couple of methods.

These notebooks can be used to transform radargrams to seg-y files and import them into [OpendTect](https://github.com/OpendTect/OpendTect) to obtain interpretable seismic-like sections:

![radargrams-3d](images/shot.png  "radargrams-3d")

This is a working repository, notebooks are experimental and used for PLANMAP activities.

The python module sharpy collects some simple methods useful to download and manage sharad radargrams.

The notebooks folder contains some examples of its application.

In particular, this simple module and notebooks shows how it is possible to:

- **GenerateAllTracksDB.ipynb** load a set of *geom* files from sharad into an unique shapefile. The tracks are simplified to reach a reasonable size. in *data* folder the output is collected for any user that just need this data.
- **FindTracks.ipynb** use a polygon to query the whole db of tracks to identify relevant tracks crossing the region of interest and save as a csv file the ID of the relevant tracks.

- **DownloadListOfSharad.ipynb**  download a list of sharad radargrams IDs from the ftp server.

- **Geoms2Package.ipynb** create a single geopackage containing sharad points of acquisition from the *geom* files as Point features, one layer for each radargram's track. 

- **DownloadAndConvert.ipynb** download and convert to seg-y radargrams in tiff format. See also **autocrop.ipynb** for this with automated cropping to the ROI.

Additional notebooks contain material that can be relevant to operate on sharad data.


# Relevant projects:
- https://github.com/adamoferro/sofa/ and https://github.com/adamoferro/dsarsim

