import numpy as np
# for plotting results
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
# for resizing and resampling
from scipy.ndimage import interpolation
# for the quantization
from sklearn.metrics import pairwise_distances_argmin
# for exporting to SEGY
from obspy.core import Trace, Stream, Stats
from obspy.io.segy.segy import SEGYBinaryFileHeader, SEGYTraceHeader
import datetime

def crop_section(image, minh, maxh, minz=2200, maxz=2600):
    return image[:,minh:maxh+1][minz:maxz, :]

def assemply_segy(image, xStart, xEnd, yStart, yEnd, dt=0.01 , scaler=1000):
    data = np.asarray(image,dtype=np.float32)
    nrows,ncols = image.shape
    # create linearly interpolated sequence of points between the two ends of the line
    traces = np.arange(ncols)
    X = np.interp(traces,[0,ncols-1],[xStart,xEnd])
    Y = np.interp(traces,[0,ncols-1],[yStart,yEnd])
    
    # create coordinate vectors with applied scaling factor
    Xint = np.round(X*scaler).astype(np.int)
    Yint = np.round(Y*scaler).astype(np.int)

    
    # Make a new Stream object
    out = Stream() 
    # For each column in the image, create a new trace
    for i,t in enumerate(data.T):       
        trace = Trace(t, header={'delta': dt }) 
        out.append(trace)
        
    # create trace headers with trace coordinates
    for i,trace in enumerate(out):
        trace.stats.segy = {}
        trace.stats.segy.trace_header = SEGYTraceHeader()

        trace.stats.segy.trace_header.trace_sequence_number_within_line = i+1
        trace.stats.segy.trace_header.sample_interval_in_ms_for_this_trace = dt
        trace.stats.segy.trace_header.number_of_samples_in_this_trace = len(trace)
        trace.stats.segy.trace_header.scalar_to_be_applied_to_all_coordinates = -1*scaler
        trace.stats.segy.trace_header.delay_recording_time = 0
        trace.stats.segy.trace_header.source_coordinate_x= Xint[i]
        trace.stats.segy.trace_header.source_coordinate_y= Yint[i]
    #     trace.stats.segy.trace_header.source_coordinate_x= X[i]
    #     trace.stats.segy.trace_header.source_coordinate_y= Y[i]
        trace.stats.segy.trace_header.x_coordinate_of_ensemble_position_of_this_trace= Xint[i]
        trace.stats.segy.trace_header.y_coordinate_of_ensemble_position_of_this_trace=Yint[i]

    #     trace.stats.segy.trace_header.x_coordinate_of_ensemble_position_of_this_trace= X[i]
    #     trace.stats.segy.trace_header.y_coordinate_of_ensemble_position_of_this_trace=Y[i]
    
    # create text header
    text_header = '{0:<80}'.format("File created on "+datetime.date.today().isoformat())
    text_header += '{0:<80}'.format("Coordinates of the line:")
    text_header += '{0:<80}'.format("LeftX   : "+ str(int(X[0])))
    text_header += '{0:<80}'.format("LeftY   : "+ str(int(Y[0])))
    text_header += '{0:<80}'.format("RightX  : "+ str(int(X[-1])))
    text_header += '{0:<80}'.format("RightY  : "+ str(int(Y[-1])))

    # Add text and binary headers to stream
    out.stats = Stats(dict(textual_file_header=text_header.encode('utf-8')))
    out.stats.binary_file_header = SEGYBinaryFileHeader()
    out.stats.binary_file_header.number_of_data_traces_per_ensemble = 1
    out.stats.binary_file_header.number_of_samples_per_data_trace = len(trace)
    
    return out

def save_segy( stream, filename="section.sgy" ):
    stream.write(filename, format='SEGY', data_encoding=5) 
