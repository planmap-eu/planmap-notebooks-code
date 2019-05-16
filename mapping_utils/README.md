# Geological Mapping

This folder contains python code for managing geological maps from python.

# Mappy project

See **ProcessMapUsingGeopandas.ipynb**.

Creating geological maps from limits and points - proof of concept with python gis tools

The idea is to start from contacts + labelled points to obtain consistent geological maps. in this way:

![woops, missing image](images/example.png)


The output can be seen in this [geopackage](notebooks/output-map-data.gpkg)

# Additional Notebooks

provide additional code for geopackage creation / management, etc:


- **ShowColors.ipynb** plot colors for legend from a pandas DataFrame for easy point and pick rgb colors when styling maps.

- **AlterEntryInFields.ipynb** Replace a given string with another in a geodatabase/layer/column. Useful to correct wrong legend entries.

- **PackGeopackage*.ipynb** Shows how geopackages can be created programmatically from python code to simplify the creation of map deliverables.

- **InsertStylesInGeopackage.ipynb** EPERIMENTAL try to insert qml and std style files into a geopackage by sql query.

- **MergeDatasetWithExel** add new columns to geopackage's layer via a JOIN operation with data coming from Excel.

other notebooks might contain relevant code that might be useful.