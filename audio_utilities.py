## Audio utilities to handle music production code
from math import log10
from scipy.signal import resample
import numpy as np
import soundfile as sf

def linear_amplitude_to_dBFS(amplitude):
    return 20 * log10(amplitude)

def dBFS_to_linear_amplitude(dBFS):
    return pow(10, dBFS/20)

def resample_audio(audio_data, original_sr, target_sr):
    # Compute the resampling ratio
    resampling_ratio = target_sr / original_sr

    # Resample the audio data
    resampled_audio = resample(audio_data, int(len(audio_data) * resampling_ratio))

    return resampled_audio

def mono_to_dual_mono(mono_signal):
    # Duplicate the mono signal into two channels
    left_channel = mono_signal
    right_channel = mono_signal.copy()  # Make a copy to avoid modifying the original array
    
    # Return the dual mono signal
    return np.vstack((left_channel, right_channel))

def normalize(tracks):
    print("Normalizing audio tracks...")
    for tid, track in tracks.items():
        # Find the maximum absolute value in the audio data
        max_amplitude = np.max(np.abs(track))
    
        # Scale the audio data to have maximum absolute value of 1
        normalized_audio = track / max_amplitude
    
        tracks[tid] = normalized_audio

    return tracks

def detect_audio_properties(audio_file):
    ob = sf.SoundFile(audio_file)
    num_channels = ob.channels
    #print("%s   SR:%s   BD: %s   NumChannels: %s"%(audio_file, ob.samplerate, ob.subtype, ob.channels))
    subtype = ob.subtype
    if subtype == "FLOAT":
        bit_depth = 32
    elif subtype == "PCM_24":
        bit_depth = 24
    elif subtype == "PCM_16":
        bit_depth = 16
    else:
        raise ValueError("Unsupported bit depth")
    return bit_depth, num_channels
