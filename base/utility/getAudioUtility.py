import os, wave
import numpy as np
import matplotlib
matplotlib.use('Agg')
import librosa
import matplotlib.pyplot as plt
import scipy.io.wavfile as wavfile
from scipy.signal import spectrogram
import platform, pathlib
from pathlib import PureWindowsPath, PurePosixPath

def get_audio_path(audio_file, folder):
    base_name = os.path.splitext(os.path.basename(audio_file.name))[0]
    base_dir = os.path.dirname(audio_file.path)

    image_path = os.path.join(f"{base_dir}/{folder}/", f"{base_name}_{folder}.jpg")
    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    if platform.system().lower() == 'windows':
        return PureWindowsPath(image_path)
    return PurePosixPath(image_path)

def get_audio_url(audio_file, folder):
    base_name = os.path.splitext(os.path.basename(audio_file.name))[0]
    return os.path.join(f"audios/{folder}", f"{base_name}_{folder}.jpg")

def get_audio_channels(audio_path):
    y, sr = librosa.load(audio_path, sr=None)
    channels = y.shape[0] if len(y.shape) == 2 else 1
    return channels

def getSpectrogram(audio_file):
    channel = get_audio_channels(audio_file.path)
    
    if channel == 1:
        try:
            raw = wave.open(audio_file.path)
        except:
            raise TypeError("Unsupported format")
        signal = raw.readframes(-1)
        signal = np.frombuffer(signal, dtype="int16")
        f_rate = raw.getframerate()
        plt.figure()
        plt.specgram(signal, Fs=f_rate, cmap="viridis", aspect="auto")
    elif channel == 2:
        sample_rate, data = wavfile.read(audio_file.path)
        data = data.T
        combined_data = np.mean(data, axis=0)
        _, _, Sxx = spectrogram(combined_data, fs=sample_rate)
        plt.figure()
        plt.specgram(combined_data, Fs=sample_rate, cmap='viridis')
    else:
        raise ValueError("Unsupported channel")
    
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.title('Spectrogram')
    plt.savefig(get_audio_path(audio_file, "spectrogram"))
    plt.close()

    return get_audio_url(audio_file, "spectrogram")

def getFrequencySpectrum(audio_file):
    try:
        data, sample_rate = librosa.load(audio_file.path, sr=44100)
    except librosa.exc.LibrosaError as e:
        raise TypeError(f"LibrosaError: {e}")
    except Exception as e:
        raise TypeError(f"Unsupported error: {e}")
    
    noverlap = 128
    nfft = 512
    stft = np.abs(librosa.stft(data, hop_length=noverlap, n_fft=nfft))

    plt.figure()
    plt.title('Audio Frequency Spectrum')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.pcolormesh(np.log10(stft), cmap='jet')
    plt.colorbar()
    plt.savefig(get_audio_path(audio_file, "spectrum_diagram"))
    plt.close()

    return get_audio_url(audio_file, "spectrum_diagram")