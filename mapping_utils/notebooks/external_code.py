# Create function to clip point data using geopandas
# https://github.com/geopandas/geopandas/issues/821

def clip_points(shp, clip_obj):
    '''
    Docs Here
    '''

    poly = clip_obj.geometry.unary_union
    return(shp[shp.geometry.intersects(poly)])

# Create function to clip line and polygon data using geopandas


def clip_line_poly(shp, clip_obj):
    '''
    docs
    '''

    # Create a single polygon object for clipping
    poly = clip_obj.geometry.unary_union
    spatial_index = shp.sindex

    # Create a box for the initial intersection
    bbox = poly.bounds
    # Get a list of id's for each road line that overlaps the bounding box and subset the data to just those lines
    sidx = list(spatial_index.intersection(bbox))
    shp_sub = shp[shp.index.isin(sidx)]

    # Clip the data - with these data
    shp_sub['geometry'] = shp_sub.intersection(poly)

    # Return the clipped layer with no null geometry values
    return shp_sub[shp_sub.geometry.notnull()]

## I just updated the above as I realized I could do this with one less line by updating the geometry col

# Final clip function that handles points, lines and polygons


def clip_shp(shp, clip_obj):
    '''
    '''
    if shp["geometry"][0].type == "Point":
        return(clip_points(shp, clip_obj))
    else:
        return(clip_line_poly(shp, clip_obj))
