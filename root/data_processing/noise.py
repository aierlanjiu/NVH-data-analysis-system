import numpy as np
import matplotlib.pyplot as plt
import librosa
from scipy import signal
from ipywidgets import interact, widgets
from IPython.display import display
import IPython.display as ipd
import subprocess
import tkinter as tk


def noise():
    audio_file = "D:\\NVH data analysis system_modified\\root\\data\\Project\\OriginalData\\noise data\\noise.wav"
    y, sr = librosa.load(audio_file)
    length = len(y) / sr
    print("音频长度：", length)

    freq_res = 8
    time_res = 0.25/freq_res

    # 计算 n_fft 和 hop_length
    n_fft = int(round(sr / freq_res))
    hop_length = int(round(sr * time_res))
    overlap_ratio = 1 - hop_length / n_fft
    print("重叠率：", overlap_ratio)
    window = librosa.filters.get_window('hamming', n_fft)

    time_res, freq_res = librosa.core.frames_to_time(1, sr=sr, hop_length=hop_length), sr / n_fft
    print("时间分辨率：", time_res)
    num_frames = int(np.ceil((len(y) - n_fft) / hop_length)) + 1
    print("频谱数：", num_frames)

    frequencies = librosa.fft_frequencies(sr=sr, n_fft=n_fft)
    a_weighting = librosa.A_weighting(frequencies)

    frame_length = n_fft

    S = librosa.stft(y, n_fft=n_fft, hop_length=hop_length, window=window)
    db_spec = librosa.amplitude_to_db(np.abs(S), ref=20*10**(-6))

    a_weighted_db_spec = (db_spec + a_weighting[:, np.newaxis])
    overall_db = np.mean(a_weighted_db_spec, axis=0)

    output = widgets.Output()

    plt.figure(figsize=(12, 10))

    length = len(y)

    def apply_filter(low_cutoff_freq, high_cutoff_freq, filter_type):

        nyquist_freq = 0.5 * sr
        low_normal_cutoff = low_cutoff_freq / nyquist_freq
        high_normal_cutoff = high_cutoff_freq / nyquist_freq

        if filter_type == 'bandpass':
            b, a = signal.butter(4, [low_normal_cutoff, high_normal_cutoff], btype=filter_type, analog=False)
        else:
            b, a = signal.butter(4, low_normal_cutoff, btype=filter_type, analog=False)

        filtered_audio = signal.lfilter(b, a, y)
        
        ipd.clear_output(wait=True)
        ipd.display(ipd.Audio(filtered_audio, rate=sr))

    low_cutoff_slider = widgets.FloatSlider(value=800, min=20, max=800, step=100, description='Low Cutoff (Hz):')
    high_cutoff_slider = widgets.FloatSlider(value=1500, min=1500, max=8000, step=100, description='High Cutoff (Hz):')
    filter_type_dropdown = widgets.Dropdown(options=['lowpass', 'highpass', 'bandpass'], description='Filter Type:')

    def update_filter(low_cutoff, high_cutoff, filter_type):
        apply_filter(low_cutoff, high_cutoff, filter_type)

    interact(update_filter, low_cutoff=low_cutoff_slider, high_cutoff=high_cutoff_slider, filter_type=filter_type_dropdown)

    def update_progress(progress):
        with output:
            ipd.clear_output(wait=True)

            plt.clf() 
            ipd.display(ipd.Audio(y, rate=sr, autoplay=True))


    progress_slider = widgets.FloatSlider(value=0.0, min=0.0, max=1.0, step=0.01, description='Playback Progress:')

    widgets.interactive(update_progress, progress=progress_slider)

    librosa.display.specshow(a_weighted_db_spec, y_axis='linear', x_axis='time', sr=sr, hop_length=hop_length, label='A-weighted Spectrogram (dB)')
    plt.colorbar(format='%+2.0f dB')
    plt.clim(80, 150)
    plt.title('A-weighted Spectrogram (dB)')
    plt.xlabel('Time (s)')
    plt.xlim(30, 60)  # Adjust the time range as needed
    plt.ylabel('Frequency (Hz)')
    plt.ylim(0, 3000)  # Adjust the frequency range as needed
    plt.show()


if __name__ == "__main__":
    noise()