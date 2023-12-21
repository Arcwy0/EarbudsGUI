import dearpygui.dearpygui as dpg
import pandas as pd
import numpy as np
from tools_plotting import *

dpg.create_context()

def load_data(file_path):
    # Load data using pandas to handle empty values
    df = pd.read_csv(file_path, delimiter=',', header=None)
    
    # Drop rows with any empty values
    df_norm = df_full_transform(df)
    df_norm = passband_filter_wrapper(df_norm)

    # Convert the cleaned DataFrame back to a NumPy array
    data = df_norm.to_numpy()
    #print(data)
    return data

def generate_channel_data(data, channel_index):
    channel_data = data[:, channel_index]
    return channel_data.tolist()

def plot_average_data(type = 'channels'): #type: 'channels' or 'fft'
    data = load_data("OpenBCI-RAW-con1_ec.txt")
    avg = np.mean(data,axis=1)
    if type == 'channels':
        with dpg.window(pos=(10, 10), label="Average from channels"):
            with dpg.plot(label="Average from channels", height=150, width=450):
                dpg.add_plot_axis(dpg.mvXAxis, label="Time", tag="Time")
                dpg.add_plot_axis(dpg.mvYAxis, label="muV", tag="muV")
                plot = dpg.add_line_series(x= np.arange(stop = len(avg)), y=avg, tag="Time_f", parent="muV")
    if type == 'fft':
        with dpg.window(pos=(560, 10), label="Average FFT"):
            frequency, amplitude = do_fft(avg)
            with dpg.plot(label="Average FFT", height=150, width=450):
                dpg.add_plot_axis(dpg.mvXAxis, label="Frequency", tag="Frequency")
                dpg.add_plot_axis(dpg.mvYAxis, label="Amplitude", tag="Amplitude")

                plot = dpg.add_line_series(x= frequency, y=amplitude, tag="FFT", parent="Amplitude")
    return plot

def load_channel(channel_index):
    data = load_data("OpenBCI-RAW-con1_ec.txt")
    channel_data = generate_channel_data(data, channel_index)
    # print(channel_data)
    # Update the line series dynamically
    # plot_tag = f'line_{channel_index}'
    x_values = list(range(len(channel_data)))
    #print(x_values)
    #dpg.configure_item('line', x=x_values, y=channel_data)
    #dpg.configure_item(plot_tag, x=x_values, y=channel_data)
    
    # Adjust the y-axis limits based on data range
    y_min, y_max = min(channel_data), max(channel_data)
    # dpg.configure_item(f"yaxis_{channel_index}", min_limit=y_min, max_limit=y_max)
    return x_values, channel_data

def plot_graphs(type = 'channels'): #type: 'channels' or 'fft'
    if type == 'channels':
        for channel_index in range(8):
            with dpg.window(pos=(10, 10 + 60 * channel_index), label=f"Channel {channel_index + 1}"):
                with dpg.plot(label=f'Channel {channel_index + 1}', height=200, width=550):
                    dpg.add_plot_axis(dpg.mvXAxis, label="Time", tag=f"xaxis_{channel_index}")
                    dpg.add_plot_axis(dpg.mvYAxis, label="muV", tag=f"yaxis_{channel_index}")
                    data_x, data_y = load_channel(channel_index)

                    #dpg.add_line_series(x=data_x, y=data_y, tag=f'line_{channel_index}', parent=f"yaxis_{channel_index}")
                    plot = dpg.add_line_series(x=data_x, y=data_y, tag=f'line_{channel_index}', parent=f"yaxis_{channel_index}")
    if type == 'fft':
        for channel_index in range(8):
            with dpg.window(pos=(560, 10 + 60 * channel_index), label=f"Channel {channel_index + 1}"):
                with dpg.plot(label=f'Channel {channel_index + 1}', height=200, width=550):
                    dpg.add_plot_axis(dpg.mvXAxis, label="Frequency", tag=f"xaxis_{channel_index}_fft")
                    dpg.add_plot_axis(dpg.mvYAxis, label="Amplitude", tag=f"yaxis_{channel_index}_fft")
                    data_x, data_y = load_channel(channel_index)
                    frequency, amplitude = do_fft(data_y)
                    plot = dpg.add_line_series(x=frequency, y=amplitude, tag=f'line_{channel_index}_fft', parent=f"yaxis_{channel_index}_fft")
                    #dpg.add_checkbox(label="Auto-fit axis limits", tag="auto_fit_checkbox", default_value=False)
    return plot

dpg.create_viewport(width=1920, height=1366, title='Updating plot data')

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
