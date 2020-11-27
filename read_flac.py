import numpy as np
import soundfile as sf

def read_flac(file, chunk = None, **kwargs):
    '''
    Reads .flac files with sf.read in a manner that returns all
    samples instead of an empty array. Can actually be used for
    any other file format readable by sf.read as well, but may
    not be as fast.
    
    This function is a workaround for the following issues:
    https://github.com/libsndfile/libsndfile/issues/431
    https://github.com/bastibe/python-soundfile/issues/236
    
    ======
    Inputs
    ======
    
    file : str
        The path of the (.flac) file to read from.
        
    chunk : int or None
        The number of frames of the (.flac) file to read at
        a time. If None, it will be set to (2**24)//n_channels,
        where n_channels is the number of channels in the .flac
        file to read from. Note that 2**24 is equal to the
        magic number 0x1000000 used as the read size for .flac
        files in soundfile.
    
    **kwargs : dict
        Extra keyword arguments to be passed to sf.read.
    
    =======
    Outputs
    =======
    
    x : numpy.ndarray
        A numpy array containing the audio data read from the
        (.flac) file.
    
    sr : int
        The sampling rate of the (.flac) file.
        
    =====
    Notes
    =====
    
    This function depends on the packages numpy and soundfile.
    Please email Kenneth Ooi (wooi002@e.ntu.edu.sg) if you
    discover any bugs or errors in implementation, thanks!
    '''
    ## SET CHUNK SIZE
    x, sr = sf.read(file, start = 0, stop = 0, **kwargs) # Used to get n_channels
    n_channels = x.shape[1] if len(x.shape) == 2 else 1
    if n_channels in [1,2,4,8]: # sf.read works normally for n_channels being powers of 2
        return sf.read(file, **kwargs)
    elif chunk is None:
        chunk = (2**24)//n_channels
    
    ## READ FILE CHUNK BY CHUNK IF n_channels IS NOT A POWER OF 2.
    parts = []
    n_frames = 0
    i = 0
    end_reached = False
    while not end_reached:
        x, sr = sf.read(file, start = i*chunk, stop = (i+1)*chunk, **kwargs)
        if x.shape[0] != 0:
            parts.append(x)
        if x.shape[0] < chunk: # sf.read will return only as many frames (possibly 0) as there are until end of file without padding.
            end_reached = True
        n_frames += x.shape[0]
        i += 1
    
    ## INITIALISE ARRAY FOR FASTER ALLOCATION
    x = np.zeros((n_frames, n_channels))
    start = 0
    stop = len(parts[0])
    for part in parts:
        x[start:stop,:] = part
        start = stop
        stop = min(stop + chunk,n_frames)
    
    ## RETURN OUTPUTS IN SAME STYLE AS sf.read
    return x, sr
