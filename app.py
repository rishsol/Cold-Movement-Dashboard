import pickle
import copy
import pathlib
import dash
import math
import datetime as dt
import pandas
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.tools as tls
import plotly.graph_objs as go
import statistics
from sklearn.preprocessing import Normalizer

app = dash.Dash(__name__)

data = 'RawArduinoData.xlsx'
df_temp_data = pandas.read_excel(data, 'Temp (optical and thermocouple)')
df_temp_data.dropna(inplace=True)
df_temp_data.reset_index(inplace=True)
df_temp_data.drop('index', axis=1, inplace=True)

for i in range(0, len(df_temp_data)):
    temp = str(df_temp_data['Ambient Temperature'][i])
    if '*C' in temp:
        df_temp_data.drop(i, inplace=True)
        
df_temp_data.reset_index(inplace=True)
df_temp_data.drop('index', axis=1, inplace=True)

for i in range(0, len(df_temp_data)):
    atemp = df_temp_data['Ambient Temperature'][i]
    atemp = atemp[10:15]
    df_temp_data['Ambient Temperature'][i] = float(atemp)

    otemp = df_temp_data['Object Temperature'][i]
    otemp = otemp[9:14]
    df_temp_data['Object Temperature'][i] = float(otemp)

df_temp_data['Reading No.'] = pandas.Series(list(range(len(df_temp_data))))

                                    ######
                                    
ds_temp_difference = df_temp_data['Object Temperature'] - df_temp_data['Ambient Temperature']

varianceTemp = 0
TEMP_DIFF_MEAN = ds_temp_difference.mean()
for i in range(len(ds_temp_difference)):
    varianceTemp = varianceTemp + ((TEMP_DIFF_MEAN - ds_temp_difference[i]) ** 2)

sdTemp = (varianceTemp/len(ds_temp_difference)) ** 0.5
colors = ['green',] * len(ds_temp_difference)
for i in range(len(colors)):
    if (TEMP_DIFF_MEAN + sdTemp <= ds_temp_difference[i]):
        colors[i] = 'red'
    
fig1 = go.Figure(data=[go.Bar(
    x=0.5 * df_temp_data['Reading No.'],
    y=ds_temp_difference,
    marker_color=colors
)])

fig1.update_layout(
title= 'Difference in Object and Ambient Temperature over time',
xaxis_title='Time (secs)',
yaxis_title='Temperature (*F)'
)

fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=0.5 * df_temp_data['Reading No.'], y=df_temp_data['Ambient Temperature'],
                    mode='lines',
                    name='Ambient Temperature'))
fig3.add_trace(go.Scatter(x=0.5 * df_temp_data['Reading No.'], y=df_temp_data['Object Temperature'],
                    mode='lines',
                    name='Object Temperature'))
                    
fig3.update_layout(
title= 'Ambient vs Object Temperature over time',
xaxis_title='Time (secs)',
yaxis_title='Temperature (*F)'
)
                    
                                ##########

df_anglestable_data = pandas.read_excel(data, 'Angle Stable')
df_anglestable_data.drop('Unnamed: 1', axis=1, inplace=True)
df_anglestable_data.drop('Unnamed: 2', axis=1, inplace=True)

for i in range(0, len(df_anglestable_data)):
    temp = str(df_anglestable_data['Angle'][i])
    if '----' in temp:
        df_anglestable_data.drop(i, inplace=True)

df_anglestable_data.reset_index(inplace=True)
df_anglestable_data.drop('index', axis=1, inplace=True)

dsXList = []
dsYList = []
dsZList = []

for i in range(0, len(df_anglestable_data)):
    temp = df_anglestable_data['Angle'][i]
    temp = temp[8:]
    if(i % 3 == 0):
        dsXList.append(float(temp))
    elif((i  - 1) % 3 == 0):
        dsYList.append(float(temp))
    else:
        dsZList.append(float(temp))

del dsXList[0]
del dsYList[0]
del dsZList[0]

df_organized_angle_data = pandas.DataFrame()
df_organized_angle_data['X Angle'] = pandas.Series(dsXList)
df_organized_angle_data['Y Angle'] = pandas.Series(dsYList)
df_organized_angle_data['Z Angle'] = pandas.Series(dsZList)
df_organized_angle_data['Time'] = pandas.Series(list(range(len(df_organized_angle_data))))

stable_meanx = df_organized_angle_data['X Angle'].mean()
stable_sdx = statistics.stdev(df_organized_angle_data['X Angle'])

stable_meany = df_organized_angle_data['Y Angle'].mean()
stable_sdy = statistics.stdev(df_organized_angle_data['Y Angle'])

stable_meanz = df_organized_angle_data['Z Angle'].mean()
stable_sdz = statistics.stdev(df_organized_angle_data['Z Angle'])


fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=0.5 * df_organized_angle_data['Time'], y=df_organized_angle_data['X Angle'],
                    mode='lines+markers',
                    name='X Angle'))
fig2.add_trace(go.Scatter(x=0.5 * df_organized_angle_data['Time'], y=df_organized_angle_data['Y Angle'],
                    mode='lines',
                    name='Y Angle'))
fig2.add_trace(go.Scatter(x=0.5 * df_organized_angle_data['Time'], y=df_organized_angle_data['Z Angle'],
mode='lines+markers',
name='Z Angle'))

fig2.update_layout(
title= 'Stable Angle',
xaxis_title='Time (secs)',
yaxis_title='Angle (degrees)'
)

                    ##########################################
df_angletilt = pandas.read_excel(data, 'Angle Tilting')

#df_angletilt.dropna(axis=1, inplace=True)
df_angletilt.drop(['Unnamed: 0', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 5', 'Unnamed: 6'], axis=1, inplace=True)

for i in range(0, len(df_angletilt)):
    angle1 = str(df_angletilt["Tilt 1"][i])
    angle2 = str(df_angletilt["Tilt 2"][i])
    if '---' in angle1 or '---' in angle2:
        df_angletilt.drop([i], axis=0, inplace=True)

df_angletilt.reset_index(inplace=True)
df_angletilt.drop('index', axis=1, inplace=True)

df_angletilt.drop([3,4,5], axis=0, inplace=True)
df_angletilt.reset_index(inplace=True)
df_angletilt.drop('index', axis=1, inplace=True)

dsXListTilt1 = []
dsYListTilt1 = []
dsZListTilt1 = []
dsTimeTilt1 = [0]

for i in range(0, len(df_angletilt)):
    if (not isinstance(df_angletilt['Tilt 1'][i], float)):
        angle = df_angletilt['Tilt 1'][i]
        angle = angle[8:]
        if(i % 3 == 0):
            dsXListTilt1.append(float(angle))
        elif((i  - 1) % 3 == 0):
            dsYListTilt1.append(float(angle))
        else:
            dsZListTilt1.append(float(angle))

df_angletilt_revised1 = pandas.DataFrame()

df_angletilt_revised1['X Angle'] = pandas.Series(dsXListTilt1)
df_angletilt_revised1['Y Angle'] = pandas.Series(dsYListTilt1)
df_angletilt_revised1['Z Angle'] = pandas.Series(dsZListTilt1)

list_to_append1 = list(range(2, len(df_angletilt_revised1) + 1) )
dsTimeTilt1 = dsTimeTilt1 + list_to_append1

df_angletilt_revised1['Time'] =  pandas.Series(dsTimeTilt1)

color_x1 = ['blue',] * len(df_angletilt_revised1['X Angle'])
color_y1 = ['red',] * len(df_angletilt_revised1['Y Angle'])
color_z1 = ['green',] * len(df_angletilt_revised1['Z Angle'])

for i in range(len(df_angletilt_revised1)):
    if (stable_meanx + (4 * stable_sdx) <= df_angletilt_revised1['X Angle'][i] or
    stable_meanx - (4 * stable_sdx) >= df_angletilt_revised1['X Angle'][i]):
        color_x1[i] = 'black'

    if (stable_meany + (4 * stable_sdy) <= df_angletilt_revised1['Y Angle'][i] or
    stable_meany - (4 * stable_sdy) >= df_angletilt_revised1['Y Angle'][i]):
        color_y1[i] = 'black'
    
    if (stable_meanz + (4 * stable_sdz) <= df_angletilt_revised1['Z Angle'][i] or
    stable_meanz - (4 * stable_sdz) >= df_angletilt_revised1['Z Angle'][i]):
        color_z1[i] = 'black'


fig4 = go.Figure()
fig4.add_trace(go.Scatter(x=0.5 * df_angletilt_revised1['Time'], y=df_angletilt_revised1['X Angle'],
                    mode='lines+markers',
                    name='X Angle', 
                    marker_color = color_x1))
fig4.add_trace(go.Scatter(x=0.5 * df_angletilt_revised1['Time'], y=df_angletilt_revised1['Y Angle'],
                    mode='lines+markers',
                    name='Y Angle',
                    marker_color= color_y1))
fig4.add_trace(go.Scatter(x=0.5 * df_angletilt_revised1['Time'], y=df_angletilt_revised1['Z Angle'],
mode='lines+markers',
name='Z Angle', 
marker_color=color_z1))

fig4.update_layout(
title= 'Tilt1',
xaxis_title='Time (secs)',
yaxis_title='Angle (degrees)'
)

                            ############
dsXListTilt2 = []
dsYListTilt2 = []
dsZListTilt2 = []

for i in range(0, len(df_angletilt)):
    if (not isinstance(df_angletilt['Tilt 2'][i], float)):
        angle = df_angletilt['Tilt 2'][i]
        angle = angle[8:]
        if(i % 3 == 0):
            dsXListTilt2.append(float(angle))
        elif((i  - 1) % 3 == 0):
            dsYListTilt2.append(float(angle))
        else:
            dsZListTilt2.append(float(angle))

df_angletilt_revised2 = pandas.DataFrame()

df_angletilt_revised2['X Angle'] = pandas.Series(dsXListTilt2)
df_angletilt_revised2['Y Angle'] = pandas.Series(dsYListTilt2)
df_angletilt_revised2['Z Angle'] = pandas.Series(dsZListTilt2)
df_angletilt_revised2['Time'] = pandas.Series(dsTimeTilt1 + [30, 31, 32])

color_x2 = ['blue',] * len(df_angletilt_revised2['X Angle'])
color_y2 = ['red',] * len(df_angletilt_revised2['Y Angle'])
color_z2 = ['green',] * len(df_angletilt_revised2['Z Angle'])

for i in range(len(df_angletilt_revised2)):
    if (stable_meanx + (4 * stable_sdx) <= df_angletilt_revised2['X Angle'][i] or
    stable_meanx - (4 * stable_sdx) >= df_angletilt_revised2['X Angle'][i]):
        color_x2[i] = 'black'

    if (stable_meany + (4 * stable_sdy) <= df_angletilt_revised2['Y Angle'][i] or
    stable_meany - (4 * stable_sdy) >= df_angletilt_revised2['Y Angle'][i]):
        color_y2[i] = 'black'
    
    if (stable_meanz + (4 * stable_sdz) <= df_angletilt_revised2['Z Angle'][i] or
    stable_meanz - (4 * stable_sdz) >= df_angletilt_revised2['Z Angle'][i]):
        color_z2[i] = 'black'


fig5 = go.Figure()
fig5.add_trace(go.Scatter(x=0.5 * df_angletilt_revised2['Time'], y=df_angletilt_revised2['X Angle'],
                    mode='lines+markers',
                    name='X Angle',
                    marker_color=color_x2))
fig5.add_trace(go.Scatter(x=0.5 * df_angletilt_revised2['Time'], y=df_angletilt_revised2['Y Angle'],
                    mode='lines+markers',
                    name='Y Angle',
                    marker_color=color_y2))
fig5.add_trace(go.Scatter(x=0.5 * df_angletilt_revised2['Time'], y=df_angletilt_revised2['Z Angle'],
mode='lines+markers',
name='Z Angle',
marker_color=color_z2))

fig5.update_layout(
title= 'Tilt2',
xaxis_title='Time (secs)',
yaxis_title='Angle (degrees)'
)
                    
                            
                            ###############

df_accelerometer_data = pandas.read_excel(data, 'Accelerometer')

xpoints = []
ypoints = []
magnitude=[]
moving_median = []
moving_average = []

for i in range(len(df_accelerometer_data)):
    datapoint = df_accelerometer_data['Data'][i]
    bar = datapoint.find('|')
    datapointx = float(datapoint[3:bar])
    datapointy = float(datapoint[bar + 5:])

    xpoints.append(datapointx)
    ypoints.append(datapointy)
    magnitude.append(math.sqrt(math.pow(datapointx, 2)+ math.pow(datapointy, 2)))


df_accelerometer_data['X Acc.'] = pandas.Series(xpoints)
df_accelerometer_data['Y Acc.'] = pandas.Series(ypoints)
df_accelerometer_data['Magnitude'] = pandas.Series(magnitude)

for i in range(len(df_accelerometer_data)):
    if (i + 5 > len(df_accelerometer_data)):
        break

    median = statistics.median(df_accelerometer_data['Magnitude'][i:i+5])
    moving_median.append(median)
    moving_average.append(statistics.mean(df_accelerometer_data['Magnitude'][i:i+5]))
    
df_accelerometer_data['Moving Median']= pandas.Series(moving_median)
df_accelerometer_data['Moving Average']= pandas.Series(moving_average)

df_accelerometer_data.drop('Data', axis=1, inplace=True)
moving_median_sd = statistics.stdev(df_accelerometer_data['Moving Median'][0:662])

colorsAcc= ['green',] * len(df_accelerometer_data)

moving_mean_sd = statistics.stdev(df_accelerometer_data['Moving Average'][0:662])
moving_mean_mean = statistics.mean(df_accelerometer_data['Moving Average'][0:662])
for i in range(len(colorsAcc) - 1):
    if abs(df_accelerometer_data['Moving Average'][i] - df_accelerometer_data['Moving Average'][i+1]) > 0.01:
        colorsAcc[i] = 'red'

fig6 = go.Figure()
fig6.add_trace(go.Scatter(x = 0.5 * pandas.Series(range(len(df_accelerometer_data['Y Acc.']))),
                    y=df_accelerometer_data['Y Acc.'],
                    mode='lines',
                    name='Y Acc.'))
fig6.add_trace(go.Scatter(x= 0.5 * pandas.Series(range(len(df_accelerometer_data['Y Acc.']))),
                    y=df_accelerometer_data['X Acc.'],
                    mode='lines',
                    name='X Acc. '))
fig6.add_trace(go.Scatter(x = 0.5 * pandas.Series(range(len(df_accelerometer_data['Y Acc.']))),
                    y=df_accelerometer_data['Magnitude'],
                    mode='lines+markers',
                    name='Magnitude',
                    marker_color= colorsAcc))
fig6.add_trace(go.Scatter(x = 0.5 * pandas.Series(range(len(df_accelerometer_data['Y Acc.']))),
                    y=df_accelerometer_data['Moving Median'],
                    mode = 'lines',
                    name = 'Moving Median'))
fig6.add_trace(go.Scatter(x = 0.5 * pandas.Series(range(len(df_accelerometer_data['Y Acc.']))), 
                    y=df_accelerometer_data['Moving Average'],
                    mode = 'lines',
                    name = 'Moving Average'))

fig6.update_layout(
title= 'Acceleration over time',
xaxis_title='Time (secs)',
yaxis_title='Acceleration'
)

                      ########################
                            
app.layout = html.Div(children=[
    html.H1(children='Demo'),
    dcc.Slider(
        id='status_bar', 
        min = 0,
        max = 0.5 * df_angletilt_revised1['Time'][len(df_angletilt_revised1) -1],
        step=1,
        value=0,
    ),
    html.Div(
        id='slider-output-container'
    ),
    dcc.Graph(
        id = 'double-temp-graph',
        figure = fig3
    ),
    dcc.Graph(
        id = 'difference-graph',
        figure = fig1
    ),
    dcc.Graph(
        id = 'anglestable-graph',
        figure = fig2
    ),
    dcc.Graph(
        id = 'angletitle1',
        figure = fig4
    ),
    dcc.Graph(
        id = 'angltilt2',
        figure = fig5
    ),
    dcc.Graph(
        id = 'Acceleration',
        figure = fig6
    )
])

@app.callback(
    dash.dependencies.Output('slider-output-container', 'children'),
    [dash.dependencies.Input('status_bar', 'value')])
def update_output(value):
    temp_diff = df_temp_data['Object Temperature'] - df_temp_data['Ambient Temperature']
    temp_diff_mean = statistics.mean(temp_diff)
    temp_diff_sd = statistics.stdev(temp_diff)

    temperature = (temp_diff[value] - temp_diff_mean) / temp_diff_sd

    avg_angle_meanx = statistics.mean(df_angletilt_revised1['X Angle'])
    avg_angle_sdx = statistics.stdev(df_angletilt_revised1['X Angle'])

    tilt1_anglex = (abs(avg_angle_meanx - df_angletilt_revised1['X Angle'][value])) / avg_angle_sdx

    avg_angle_meany = statistics.mean(df_angletilt_revised1['Y Angle'])
    avg_angle_sdy = statistics.stdev(df_angletilt_revised1['Y Angle'])

    tilt1_angley = (abs(avg_angle_meany - df_angletilt_revised1['Y Angle'][value])) / avg_angle_sdy

    avg_angle_meanz= statistics.mean(df_angletilt_revised1['Z Angle'])
    avg_angle_sdz = statistics.stdev(df_angletilt_revised1['Z Angle'])

    tilt1_anglez = (abs(avg_angle_meanz - df_angletilt_revised1['Z Angle'][value])) / avg_angle_sdz

    acc_avg = statistics.mean(df_accelerometer_data['Magnitude'])
    acc_sd = statistics.stdev(df_accelerometer_data['Magnitude'])

    acceleration = (abs(acc_avg - df_accelerometer_data['Magnitude'][value])) / acc_sd

    if temperature > 1:
        total = (0.5 * temperature) + (0.16 * tilt1_anglex) + (0.16 * tilt1_angley) + (0.16 * tilt1_anglez) + (0.02 * acceleration)
    else:
        total = (0.5 * 0) + (0.16 * tilt1_anglex) + (0.16 * tilt1_angley) + (0.16 * tilt1_anglez) + (0.02 * acceleration)

    if total < 0.4:
        return str(value) + ' seconds: Poor condition'
    elif total < 0.55:
        return str(value) + ' seconds: Fair condition'
    else:
        return str(value) + ' seconds: Good condition'

if __name__ == '__main__':
    app.run_server(debug=True)
