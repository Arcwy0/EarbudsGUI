from __future__ import annotations
import dearpygui.dearpygui as dpg
from typing import Callable, Dict, Iterable
import pandas as pd
import numpy as np
from tqdm import tqdm
import scipy
from scipy.signal import butter, lfilter
from scipy.signal import freqz
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

def filter_wrapper(func, df, **kwargs):
    #Should be edited
    #TODO: rewrite without subjects and classes
    """
    A wrapper function for any filter or transformation functions to apply over the entire df.
    """
    
    res_df = pd.DataFrame()
    
    for subject_id in tqdm(df["subject_id"].unique()):
        for class_id in df["class"].unique():
            tmp_df = df[(df["subject_id"] == subject_id) & (df["class"] == class_id)]
            tmp_df = tmp_df.drop(["subject_id", "class"], axis = 1)
            tmp_df = func(tmp_df, **kwargs)
            
            tmp_df["class"] = class_id
            tmp_df["subject_id"] = subject_id

            if res_df.empty:
                res_df = tmp_df

            else:
                res_df = pd.concat([res_df, tmp_df], axis = 0)

    return res_df.reset_index(drop=True)

#Normalization, standartization and other stuff
def edit_columns(df: pd.DataFrame):
    df = df.drop([8], axis = 1)
    return df
    
def normalize_df(df: pd.DataFrame, window_size: int = 100) -> pd.DataFrame:
    return (df-df.mean())/df.std()


def standardize_df(df: pd.DataFrame) -> pd.DataFrame:
    return (df - df.min()) / (df.max() - df.min())


def norm_standard_window(df: pd.DataFrame, window_size: int = 500) -> pd.DataFrame:
    tmp_df = df.reset_index(drop=True)
    res_df = df.copy()
    
    for idx in range(0, len(tmp_df), window_size):
        upper_idx = min(len(tmp_df), idx+window_size)
        window_df = tmp_df[idx: upper_idx]
        norm_window_df = normalize_df(window_df)
        norm_window_df = standardize_df(norm_window_df)
        res_df.iloc[idx:upper_idx] = norm_window_df
    
    return res_df

def seq_convolution(
                    df: pd.DataFrame,
                    kernel_size = 10,
                    kernel_type = "mean",
                    step_size = 5,
                    verbose: str = False
                    ) -> pd.DataFrame:

    index_bitmap = np.arange(len(df)) % step_size == 1
    
    if kernel_type == "max":
        res_df =  df.rolling(window=kernel_size).max()
        
    elif kernel_type == "mean":
        res_df =  df.rolling(window=kernel_size).mean()
        
    res_df = res_df[index_bitmap].dropna().reset_index(drop=True)
        
    if verbose:
        print(f"Data points reduced by: {len(df) - len(res_df)} or {round(100 * (len(df) - len(res_df)) / len(df), 3)} %")
        
    return res_df

def moving_average(
                    df: pd.DataFrame,
                    kernel_size = 50
                    ) -> pd.DataFrame:

    res_df =  df.rolling(window=kernel_size).mean()
    return res_df.dropna().reset_index(drop=True)

#TODO: Apply other transformations
def df_full_transform(df: pd.DataFrame):
    df = edit_columns(df)
    df = norm_standard_window(df)
    df = seq_convolution(df)
    df = moving_average(df)
    return df

#Signal processing

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def passband_filter(
                    signal, 
                    lowcut = 1.0, # Min frequency
                    highcut = 100.0, # Max frequency
                    fs = 250.0, # Sampling rate
                    plot = False 
                    ) -> np.array:
    
    # Sample rate and desired cutoff frequencies (in Hz).    
#     fs = len(signal)
    for order in [3, 6, 9]:
        b, a = butter_bandpass(lowcut, highcut, fs, order=order)
        w, h = freqz(b, a, worN=2000)
        
    #     if plot:
    #         plt.figure(1, figsize = figsize); plt.clf()
    #         plt.plot((fs * 0.5 / np.pi) * w, abs(h), label="order = %d" % order)

    # if plot:
    #     plt.plot([0, 0.5 * fs], [np.sqrt(0.5), np.sqrt(0.5)], '--', label='sqrt(0.5)')
    #     plt.xlabel('Frequency (Hz)'); plt.ylabel('Gain'); plt.grid(True); plt.legend(loc='best')

    # Filter a noisy signal.
#     T = 0.05
    T = len(signal) / fs
#     nsamples = T * fs
    nsamples = len(signal)
    t = np.linspace(0, T, int(nsamples), endpoint=False)
    a = 0.02
    
    # if plot:
    #     plt.figure(figsize = figsize)
    #     plt.plot(t, signal, label='Noisy signal')
    
    # Butter bandpass filter    
    filtered_signal = butter_bandpass_filter(signal, lowcut, highcut, fs, order=6)
    
    # Plot filtered results
    # if plot:
    #     plt.plot(t, filtered_signal, label=f"Filtered signal ({lowcut} Hz - {highcut} Hz)")
    #     plt.xlabel('time (seconds)')
    #     plt.hlines([-a, a], 0, T, linestyles='--')
    #     plt.grid(True); plt.axis('tight'); plt.legend(loc='upper left'); plt.show()
        
    return filtered_signal


def passband_filter_wrapper(
                            df, 
                            lowcut: float = 1.0, # Min frequency
                            highcut: float = 100.0, # Max frequency
                            fs: float = 250.0, # Sampling rate
                            plot: bool = False 
                            ) -> np.array:
    
    for col in df:
        df[col] = passband_filter(
                                df[col], 
                                lowcut, # Min frequency
                                highcut, # Max frequency
                                fs, # Sampling rate
                                plot
                                )
    return df

def do_fft(
            signal: np.array,
            sample_rate = 250
            ) -> None:
    # Number of sample points
    N = len(signal)
    # sample spacing
    T = 1.0/sample_rate
    x = np.linspace(0.0, N * T, len(signal), endpoint=False)
    y = signal
    yf = fft(y)
    xf = fftfreq(N, T)[:N//2]
    yfamp = 2.0/N * np.abs(yf[0:N//2])
    return xf,yfamp