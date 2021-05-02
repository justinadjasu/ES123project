import pandas as pd
import numpy as np
import time
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, TextInput, Select, HoverTool, Span, Legend, CheckboxGroup, TapTool, Button, CheckboxButtonGroup, Div, Toggle, TextAreaInput, DataTable, Slider, TableColumn, LassoSelectTool, ColorBar, LogColorMapper, LinearColorMapper
from bokeh.plotting import figure
from bokeh.palettes import Turbo256
from bokeh.transform import linear_cmap
from bokeh.util.hex import hexbin
from helpers import concentration_equation

# dummy counter class
class counter:
    def __init__(self, i=0):
        self.i = i
        return

count = counter()

# create widgets
widget_width = 300
afferent = Slider(title="Afferent Arteriole Pressure (mmHg)", start=50, step=1, value=55, end=70, width=widget_width)
efferent = Slider(title="Efferent Arteriole Pressure (mmHg)", start=0, step=1, end=40, value=15, width=widget_width)
conc = Slider(title="Initial Blood Concentration (mM)", value=5, start=0, step=1, end=20, width=widget_width)
production_rate = Slider(title="Rate of Production (mM/min)", value=0, start=0, step=.01, end=1, width=widget_width)
hematocrit = Slider(title="Hematocrit", value=.3, start=.10, step=.02, end=.6, width=widget_width)
blood_volume = Slider(title="Blood Volume (L)", value=5, start=2, step=.1, end=7, width=widget_width)
submit = Toggle(active=False, label="Simulate", button_type="primary", width=widget_width)
reset = Button(label='Reset to t = 0')

# submit = Button(label="Submit")
widget_head = Div(text="""<b style="text-align:center">Conditions</b><br>""", width=widget_width)

conditions_ls = ['normal', 'atherosclerosis', 'vascular stenosis', 'hypertension']
kf_dict = {'normal':3, 'atherosclerosis':3.62, 'vascular stenosis':2.46, 'hypertension':2.43}
conditions = Select(options=conditions_ls, value='normal', title="Physiological Condition")

n = 250
x = np.linspace(0, 10, n)
y = np.linspace(0, 10, n)
xx, yy = np.meshgrid(x, y)
d = np.sin(xx)*np.cos(yy)

# main column data source
data_dict = {
    'x':[],
    'y':[],
    'c':[],
    't':[]
}

data = ColumnDataSource(data=data_dict)

# create plot grid
plot_size = [600, 600]

# heatmap
heatmap = figure(plot_width=plot_size[0], plot_height=plot_size[1],
    toolbar_location=None)
heatmap.grid.visible = False
heatmap.title.text = "Concentration Over Space"
heatmap.x_range.range_padding = heatmap.y_range.range_padding = 0

heat_dict = {
    'x':[0],
    'y':[0],
    'c':[d]
}

heat_source = ColumnDataSource(data=heat_dict)

# plots of concentration vs. time
cvt = figure(plot_width=plot_size[0], plot_height=plot_size[1])
cvt.title.text = "Concentration vs. Time"
cvt.line(x='t', y='c', source=data)

# initialize solver
math = concentration_equation()
math.afferent = afferent.value
math.efferent = efferent.value
math.c = conc.value
math.production_rate = production_rate.value
math.hct = hematocrit.value
math.kf = kf_dict[conditions.value]
math.blood_volume = blood_volume.value

def update():
    
    c_val = math.progress()

    c_grid = math.surface()

    new_data_dict = {
        'x':[0],
        'y':[0],
        'c':[c_val],
        't':[math.minutes]
    }

    data.stream(new_data_dict)

    heat_source.data = {
        'x':[0],
        'y':[0],
        'c':[c_grid]
    }

    if conditions.value == 'vascular stenosis':
        math.r = 6
    else:
        math.r = 8

    if count.i == 0:
        color_mapper = LinearColorMapper(palette='Viridis256', low=np.min(c_grid), high=np.max(c_grid))
        heatmap.image(image='c', x='x', y='y', dw=10, dh=10, level='image', color_mapper=color_mapper, source=heat_source)
        count.i += 1
    
    return

def animate():
    if submit.active:
        update()
    return

def slider_update():
    switch = False
    if submit.active:
        switch = True
        submit.active = False
    math.afferent = afferent.value
    math.efferent = efferent.value
    math.production_rate = production_rate.value
    math.hct = hematocrit.value
    math.kf = kf_dict[conditions.value]
    math.blood_volume = blood_volume.value
    return

def labeler():
    if submit.active:
        submit.label = 'Pause'
    else:
        submit.label = 'Simulate'
    return

def resetter():
    data.data = {
    'x':[],
    'y':[],
    'c':[],
    't':[]
    }

    heat_source.data = {
        'x':[0],
        'y':[0],
        'c':[d]
    }
    return

update()

for widget in [afferent, efferent, conc, production_rate, hematocrit, blood_volume]:
    widget.on_change('value', lambda attr, old, new: slider_update())

submit.on_click(lambda x: labeler())
# webpage layout
widgets = column(widget_head, afferent, efferent, conc, production_rate, hematocrit, blood_volume, conditions, submit)
layout = row(widgets, heatmap, cvt)
curdoc().add_root(layout)
curdoc().add_periodic_callback(animate, 200)
