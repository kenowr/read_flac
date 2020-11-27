# read_flac
A crude workaround to libsndfile/soundfile not reading multi-channel .flac files properly.

This repository contains a simple function `read_flac` that uses `soundfile.read` in a manner that does not lead to empty arrays being read. According to the issue brought up in https://github.com/libsndfile/libsndfile/issues/431, .flac files with a number of channels not equal to 1, 2, 4, or 8 will be erroneously read by `soundfile.read`. The solution, as mentioned in the post, is to read at most `0x1000000 / n_channels` frames of a .flac file at a time if it does not have 1, 2, 4, or 8 channels. Hence, `read_flac` reads entire .flac files in chunks of `0x1000000 / n_channels` frames and concatenates them at the end to produce a numpy array as one should expect when using `soundfile.read`. The input and arguments of `read_flac` are similar to that of `soundfile.read`, and are documented in the function header itself as well as this readme.

See also: https://github.com/bastibe/python-soundfile/issues/236

    
Inputs
------
    
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
    
Outputs
-------
    
    x : numpy.ndarray
        A numpy array containing the audio data read from the
        (.flac) file.
    
    sr : int
        The sampling rate of the (.flac) file.

Contact
-------

Please email Kenneth Ooi (wooi002@e.ntu.edu.sg) if you discover any bugs or errors, thanks!
