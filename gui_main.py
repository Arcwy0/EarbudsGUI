import dearpygui.dearpygui as dpg
import pandas as pd
import numpy as np
from plotting import *

dpg.create_context()

plot_graphs(type='channels')
plot_graphs(type='fft')
#plot_average_data(type = 'channels')
#plot_average_data(type = 'fft')


dpg.create_viewport(width=1920, height=1366, title='Updating plot data')

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

