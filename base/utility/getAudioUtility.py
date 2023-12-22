import os, wave, sys, io
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wavfile
from scipy.signal import spectrogram
from PIL import Image


def getSpectrogram(audio_file):
    # Fs, aud = wavfile.read(audio_file.path)
    # # select left channel only
    # aud = aud[:,0]
    # # trim the first 125 seconds
    # first = aud[:int(Fs*125)]
    # powerSpectrum, frequenciesFound, time, imageAxis = plt.specgram(first, Fs=Fs)
    # plt.savefig(get_audio_path(audio_file, "spectrogram"))
    # return get_audio_url(audio_file, "spectrogram")

    sample_rate, data = wavfile.read(audio_file.path)
    frequencies, times, Sxx = spectrogram(data, fs=sample_rate)

    # Convert the spectrogram to decibels (adjust the scale as needed)
    Sxx_db = 10 * np.log10(Sxx)

    # Normalize the values to fit within the 8-bit image range (0 to 255)
    normalized_spectrogram = ((Sxx_db - np.min(Sxx_db)) / (np.max(Sxx_db) - np.min(Sxx_db))) * 255

    # Ensure that the data type is suitable for creating a PIL Image
    normalized_spectrogram = normalized_spectrogram.astype(np.uint8)
    image = Image.fromarray(normalized_spectrogram)
    image.save(get_audio_path(audio_file, "spectrogram"), format="jpg")
    return get_audio_url(audio_file, "spectrogram")

def get_audio_path(audio_file, folder):
    base_name = os.path.splitext(os.path.basename(audio_file.name))[0]
    base_dir = os.path.dirname(audio_file.path)
    return os.path.join(f"{base_dir}/{folder}", f"{base_name}/{folder}.jpg")

def getSpectrum_diagram(audio_file):
    raw = wave.open(audio_file.path)

    signal = raw.readframes(-1)
    signal = np.frombuffer(signal, dtype="int16")

    f_rate = raw.getframerate()
    time = np.linspace(0, len(signal)/f_rate, num=len(signal))
    plt.plot(time, signal)

    plt.savefig(get_audio_path(audio_file, "spectrum_diagram"))
    return get_audio_url(audio_file, "spectrum_diagram")

def get_audio_url(audio_file, folder):
    base_name = os.path.splitext(os.path.basename(audio_file.name))[0]
    return os.path.join(f"audios/{folder}", f"{base_name}/{folder}.jpg")