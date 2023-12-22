import os, wave, sys, io
import numpy as np
import matplotlib
matplotlib.use('Agg')
import librosa
import matplotlib.pyplot as plt
import scipy.io.wavfile as wavfile
from scipy.signal import spectrogram

def get_audio_path(audio_file, folder):
    base_name = os.path.splitext(os.path.basename(audio_file.name))[0]
    base_dir = os.path.dirname(audio_file.path)
    return os.path.join(f"{base_dir}/{folder}", f"{base_name}/{folder}.jpg")

def get_audio_url(audio_file, folder):
    base_name = os.path.splitext(os.path.basename(audio_file.name))[0]
    return os.path.join(f"/audios/{folder}", f"{base_name}/{folder}.jpg")

def get_audio_channels(audio_path):
    y, sr = librosa.load(audio_path, sr=None)
    channels = y.shape[0] if len(y.shape) == 2 else 1
    return channels

def getSpectrogram(audio_file):
    channel = get_audio_channels(audio_file.path)
    
    if channel == 1:
        raw = wave.open(audio_file.path)
        signal = raw.readframes(-1)
        signal = np.frombuffer(signal, dtype="int16")
        f_rate = raw.getframerate()
        time = np.linspace(0, len(signal)/f_rate, num=len(signal))
        plt.figure()
        plt.specgram(signal, Fs=f_rate, cmap="viridis", aspect="auto")
    else:
        sample_rate, data = wavfile.read(audio_file.path)
        data = data.T
        combined_data = np.mean(data, axis=0)
        _, _, Sxx = spectrogram(combined_data, fs=sample_rate)
        plt.figure()
        plt.specgram(combined_data, Fs=sample_rate, cmap='viridis')
    spectrogram_save_directory = os.path.join(os.path.dirname(audio_file.path), "spectrogram")
    os.makedirs(spectrogram_save_directory, exist_ok=True)
    spectrogram_path = os.path.join(spectrogram_save_directory, f"{os.path.splitext(os.path.basename(audio_file.name))[0]}_spectrogram.png")
    plt.savefig(spectrogram_path)
    plt.close()

    return get_audio_url(audio_file, "spectrogram")

