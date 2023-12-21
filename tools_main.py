import dearpygui.dearpygui as dpg
import math
from math import sin, cos
import random
import webbrowser


def _help(message):
    last_item = dpg.last_item()
    group = dpg.add_group(horizontal=True)
    dpg.move_item(last_item, parent=group)
    dpg.capture_next_item(lambda s: dpg.move_item(s, parent=group))
    t = dpg.add_text("(?)", color=[0, 255, 0])
    with dpg.tooltip(t):
        dpg.add_text(message)

def _hyperlink(text, address):
    b = dpg.add_button(label=text, callback=lambda:webbrowser.open(address))
    dpg.bind_item_theme(b, "__demo_hyperlinkTheme")

def _config(sender, keyword, user_data):

    widget_type = dpg.get_item_type(sender)
    items = user_data

    if widget_type == "mvAppItemType::mvRadioButton":
        value = True

    else:
        keyword = dpg.get_item_label(sender)
        value = dpg.get_value(sender)

    if isinstance(user_data, list):
        for item in items:
            dpg.configure_item(item, **{keyword: value})
    else:
        dpg.configure_item(items, **{keyword: value})

def _add_config_options(item, columns, *names, **kwargs):
    
    if columns == 1:
        if 'before' in kwargs:
            for name in names:
                dpg.add_checkbox(label=name, callback=_config, user_data=item, before=kwargs['before'], default_value=dpg.get_item_configuration(item)[name])
        else:
            for name in names:
                dpg.add_checkbox(label=name, callback=_config, user_data=item, default_value=dpg.get_item_configuration(item)[name])

    else:

        if 'before' in kwargs:
            dpg.push_container_stack(dpg.add_table(header_row=False, before=kwargs['before']))
        else:
            dpg.push_container_stack(dpg.add_table(header_row=False))

        for i in range(columns):
            dpg.add_table_column()

        for i in range(int(len(names)/columns)):

            with dpg.table_row():
                for j in range(columns):
                    dpg.add_checkbox(label=names[i*columns + j], 
                                        callback=_config, user_data=item, 
                                        default_value=dpg.get_item_configuration(item)[names[i*columns + j]])
        dpg.pop_container_stack()

def _add_config_option(item, default_value, *names):
    dpg.add_radio_button(names, default_value=default_value, callback=_config, user_data=item)

def _hsv_to_rgb(h, s, v):
    if s == 0.0: return (v, v, v)
    i = int(h*6.) # XXX assume int() truncates!
    f = (h*6.)-i; p,q,t = v*(1.-s), v*(1.-s*f), v*(1.-s*(1.-f)); i%=6
    if i == 0: return (255*v, 255*t, 255*p)
    if i == 1: return (255*q, 255*v, 255*p)
    if i == 2: return (255*p, 255*v, 255*t)
    if i == 3: return (255*p, 255*q, 255*v)
    if i == 4: return (255*t, 255*p, 255*v)
    if i == 5: return (255*v, 255*p, 255*q)

def _create_static_textures():
   
    ## create static textures
    texture_data1 = []
    for i in range(100*100):
        texture_data1.append(255/255)
        texture_data1.append(0)
        texture_data1.append(255/255)
        texture_data1.append(255/255)

    texture_data2 = []
    for i in range(50*50):
        texture_data2.append(255/255)
        texture_data2.append(255/255)
        texture_data2.append(0)
        texture_data2.append(255/255)

    texture_data3 = []
    for row in range(50):
        for column in range(50):
            texture_data3.append(255/255)
            texture_data3.append(0)
            texture_data3.append(0)
            texture_data3.append(255/255)
        for column in range(50):
            texture_data3.append(0)
            texture_data3.append(255/255)
            texture_data3.append(0)
            texture_data3.append(255/255)
    for row in range(50):
        for column in range(50):
            texture_data3.append(0)
            texture_data3.append(0)
            texture_data3.append(255/255)
            texture_data3.append(255/255)
        for column in range(50):
            texture_data3.append(255/255)
            texture_data3.append(255/255)
            texture_data3.append(0)
            texture_data3.append(255/255)

    dpg.add_static_texture(100, 100, texture_data1, parent="__demo_texture_container", tag="__demo_static_texture_1", label="Static Texture 1")
    dpg.add_static_texture(50, 50, texture_data2, parent="__demo_texture_container", tag="__demo_static_texture_2", label="Static Texture 2")
    dpg.add_static_texture(100, 100, texture_data3, parent="__demo_texture_container", tag="__demo_static_texture_3", label="Static Texture 3")

def _create_dynamic_textures():
    
    ## create dynamic textures
    texture_data1 = []
    for i in range(100*100):
        texture_data1.append(255/255)
        texture_data1.append(0)
        texture_data1.append(255/255)
        texture_data1.append(255/255)

    texture_data2 = []
    for i in range(50*50):
        texture_data2.append(255/255)
        texture_data2.append(255/255)
        texture_data2.append(0)
        texture_data2.append(255/255)

    dpg.add_dynamic_texture(100, 100, texture_data1, parent="__demo_texture_container", tag="__demo_dynamic_texture_1")
    dpg.add_dynamic_texture(50, 50, texture_data2, parent="__demo_texture_container", tag="__demo_dynamic_texture_2")

def _update_dynamic_textures(sender, app_data, user_data):

    new_color = app_data
    new_color[0] = new_color[0]
    new_color[1] = new_color[1]
    new_color[2] = new_color[2]
    new_color[3] = new_color[3]

    if user_data == 1:
        texture_data = []
        for i in range(100*100):
            texture_data.append(new_color[0])
            texture_data.append(new_color[1])
            texture_data.append(new_color[2])
            texture_data.append(new_color[3])
        dpg.set_value("__demo_dynamic_texture_1", texture_data)

    elif user_data == 2:
        texture_data = []
        for i in range(50*50):
            texture_data.append(new_color[0])
            texture_data.append(new_color[1])
            texture_data.append(new_color[2])
            texture_data.append(new_color[3])
        dpg.set_value("__demo_dynamic_texture_2", texture_data)

def _on_demo_close(sender, app_data, user_data):
    dpg.delete_item(sender)
    dpg.delete_item("__demo_texture_container")
    dpg.delete_item("__demo_colormap_registry")
    dpg.delete_item("__demo_hyperlinkTheme")
    dpg.delete_item("__demo_theme_progressbar")
    dpg.delete_item("stock_theme1")
    dpg.delete_item("stock_theme2")
    dpg.delete_item("stock_theme3")
    dpg.delete_item("stock_theme4")
    dpg.delete_item("stem_theme1")
    dpg.delete_item("__demo_keyboard_handler")
    dpg.delete_item("__demo_mouse_handler")
    dpg.delete_item("__demo_filedialog")
    dpg.delete_item("__demo_stage1")
    dpg.delete_item("__demo_popup1")
    dpg.delete_item("__demo_popup2")
    dpg.delete_item("__demo_popup3")
    dpg.delete_item("__demo_item_reg3")
    dpg.delete_item("__demo_item_reg6")
    dpg.delete_item("__demo_item_reg7")
    dpg.delete_item("demoitemregistry")
    for i in range(7):
        dpg.delete_item("__demo_theme"+str(i))
        dpg.delete_item("__demo_theme2_"+str(i))
    for i in range(5):
        dpg.delete_item("__demo_item_reg1_"+str(i))
        dpg.delete_item("__demo_item_reg2_"+str(i))
    for i in range(3):
        dpg.delete_item("__demo_item_reg4_"+str(i))
    for i in range(4):
        dpg.delete_item("__demo_item_reg5_"+str(i))