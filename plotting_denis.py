import dearpygui.dearpygui as dpg
import dearpygui.dearpygui as dpg
import math
import time
import random
from collections import deque
from tools_plotting import *

NUM_CHANNELS = 8

dpg.create_context()

DEQUE_MAX_LEN = 250
FFT_MAX_LEN = 250

data_x = [deque(maxlen=DEQUE_MAX_LEN) for _ in range(NUM_CHANNELS)]
data_y = [deque(maxlen=DEQUE_MAX_LEN) for _ in range(NUM_CHANNELS)]
fft_data = deque(maxlen=FFT_MAX_LEN)


def load_data(file_path):
    # Load data using pandas to handle empty values
    df = pd.read_csv(file_path, delimiter=',', header=None)
    
    # Drop rows with any empty values
    df_norm = df_full_transform(df)
    df_norm = passband_filter_wrapper(df_norm)

    # Convert the cleaned DataFrame back to a NumPy array
    data = df_norm.to_numpy()
    print(len(data))
    return data


def update_channel_plots(step,data):
    for i in range(NUM_CHANNELS):
        data_y[i].append(data[step,i])
        data_x[i].append(step)
        dpg.configure_item(f'line{i}', x=list(data_x[i]), y=list(data_y[i]))
        dpg.fit_axis_data(f"xaxis{i}")

def update_fft_plot(step,data):
    fft_data.append(np.sum(data[step,:])/NUM_CHANNELS)
    frequency, amplitude = do_fft(np.array(list(fft_data)),sample_rate=250)
    dpg.configure_item(f'line_fft', x=frequency, y=amplitude)



def plot_update():
    data = load_data("OpenBCI-RAW-con1_ec.txt")
    with dpg.window(label="EEG DATA", width=1100, height=800):
        for i in range(NUM_CHANNELS):
            channel_data = data[:,i].tolist()
            x_values=list(range(len(channel_data)))
            with dpg.plot(width=500,height=80,tag=f"plot{i}"):
                dpg.add_plot_axis(dpg.mvXAxis, parent=f"plot{i}",tag=f"xaxis{i}", time=True, no_tick_labels=True)
                dpg.add_plot_axis(dpg.mvYAxis, parent=f"plot{i}",tag=f"yaxis{i}")
                dpg.set_axis_limits(dpg.last_item(), -0.5, 0.5)
                # dpg.add_line_series(x_values,channel_data,  tag=f'line{i}', parent=f"yaxis{i}")
                dpg.add_line_series([],[],  tag=f'line{i}', parent=f"yaxis{i}")
        with dpg.plot(width=500,height=500,tag='fft',pos=(525,30)):
            dpg.add_plot_axis(dpg.mvXAxis,label='Frequency',tag='x_fft')
            dpg.set_axis_limits(dpg.last_item(),0,50)
            dpg.add_plot_axis(dpg.mvYAxis,label='Amplitude',tag='y_fft')
            dpg.set_axis_limits(dpg.last_item(),0,0.3)
            dpg.add_line_series([],[],  tag=f'line_fft', parent=f"y_fft")
        dpg.add_checkbox(label="Start exp", tag="start_exp", default_value=False)
        while dpg.is_dearpygui_running() and step < len(data):
            if dpg.get_value('start_exp'):
                update_channel_plots(step,data)
                update_fft_plot(step,data)
                step+=1
            dpg.render_dearpygui_frame()
    return True

dpg.create_viewport(title='EarBuds', width=1100, height=800)
dpg.setup_dearpygui()
dpg.show_viewport()
step = 0





dpg.destroy_context()