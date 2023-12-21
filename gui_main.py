import dearpygui.dearpygui as dpg
import pandas as pd
import numpy as np
from tools_main import *
from plotting_denis import *

NUM_CHANNELS = 8

dpg.create_context()

DEQUE_MAX_LEN = 250
FFT_MAX_LEN = 250

data_x = [deque(maxlen=DEQUE_MAX_LEN) for _ in range(NUM_CHANNELS)]
data_y = [deque(maxlen=DEQUE_MAX_LEN) for _ in range(NUM_CHANNELS)]
fft_data = deque(maxlen=FFT_MAX_LEN)

# plot_graphs(type='channels')
# plot_graphs(type='fft')
#plot_average_data(type = 'channels')
#plot_average_data(type = 'fft')

def _log(sender, app_data, user_data):
    print(f"sender: {sender}, \t app_data: {app_data}, \t user_data: {user_data}")


dpg.create_viewport(width=1920, height=1366, title='EarBuds Demo')
def show_app():
    with dpg.window(label="Earbuds Demo", width=1920, height=1366, pos=(10, 10), tag="__earbuds_main"):
        with dpg.menu_bar():

                with dpg.menu(label="Menu"):

                    dpg.add_text("This menu is just for show!")
                    dpg.add_menu_item(label="New")
                    dpg.add_menu_item(label="Open")

                    with dpg.menu(label="Open Recent"):

                        dpg.add_menu_item(label="harrel.c")
                        dpg.add_menu_item(label="patty.h")
                        dpg.add_menu_item(label="nick.py")

                    dpg.add_menu_item(label="Save")
                    dpg.add_menu_item(label="Save As...")

                    with dpg.menu(label="Settings"):

                        dpg.add_menu_item(label="Option 1", callback=_log)
                        dpg.add_menu_item(label="Option 2", check=True, callback=_log)
                        dpg.add_menu_item(label="Option 3", check=True, default_value=True, callback=_log)
        with dpg.tab_bar() as tb:

            with dpg.tab(label="Overall statistics"):
                dpg.add_text("This is the tab 2!")

            with dpg.tab(label="Update Plot") as t2:
                plot_update()

            with dpg.tab(label="Recommendations"):
                dpg.add_text("This is the tab 3!")

            with dpg.tab(label="tab 4"):
                dpg.add_text("This is the tab 4!")

            tbb = dpg.add_tab_button(label="+")
            dpg.add_tab_button(label="?")
            
show_app()
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
step = 0