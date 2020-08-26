import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import datetime

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo
import hvplot
import hvplot.pandas
import holoviews as hv
import panel as pn


# some variables
oil_rate = '*rOIL'
gas_rate = '*rGAS'
water_rate = '*WATER'
BHP = '*BHP_AVG'
BHT = '*BHT_AVG'
WHP = '*WHP_AVG_P'
WHT = '*WHT_AVG_P'
code = '*WELL_BORE_CODE'
date = '*DATE'


flatten = lambda l: [item for sublist in l for item in sublist]

def re_writer(file): # pythonexamples.org
    '''
    Rewrites data file removing '-99999' and 'Null' replacing with 0.0
    Parameters:
    file: string
        text file
    gasr: string

        gas rate column to be renamed, if not rate, use get_rate()
    oilr: string
    oil rate column to be renamed, if not rate, use get_rate()
    '''

#     file = '/dbfs/' + file # to access DataBricks file system
    fin = open(file, "rt", encoding='cp1252') # can open weird characters
    #read file contents to string
    data = fin.read()
#     data = data.replace('Null', 'null')
    data = data.replace(' -99999', 'null')
    data = data.replace('null', 'Null')
    data = data.replace('NO 6', 'NO_6')
    data = data.replace(' A', '_A')
    data = data.replace(' C', '_C')
    data = data.replace(' B', '_B')
    data = data.replace(' H', '_H')
#     data = data.replace('WELL_CODE', 'WELL_BORE_CODE')
    data = data.replace('OIL,CHOKE_SIZE_GI', 'rOIL *CHOKE_SIZE_GI')
    data = data.replace('GAS_RATE,PRODUCTIVITY_INDEX', 'rGAS *PRODUCTIVITY_INDEX')
#     data = data.replace('*', '')

    # maybe dont need these if cSchema is enough
    data = data.replace('Date', 'DATE')


    fin.close()
    #open the input file in write mode
    fin = open(file, "wt")
    #overrite the input file with the resulting data
    fin.write(data)
    fin.close()

def make_df(file_location, datatype):
    if datatype == 'test':
        print('***********Accepted test data***********')
        re_writer(file_location)
        df = pd.read_csv(file_location, header=0, sep=' ', engine='python', skiprows=2, index_col=False)
#         df = df.set_index(['*WELL_CODE'], inplace=True)
        df.drop(['Unnamed: 32'], axis=1, inplace=True)
        df.drop(['*END_DATE', '*RESULT_NO', '*END_DATE', '*RESERVOIR_PRESS', '*COND_RATE', \
                 '*STRUCTURE', '*FLUID_PI', "*GAS_LIFT", "*GAS_LIFT_GKGL", \
                 "*GAS_LIFT_RGL", "*HSV", "*QC_M", "*QG_M", "*QO_M", '*QW_M', \
                 '*SAND_TRAP', "*H2S"], axis=1, inplace=True)
        df['*DATE'] = pd.to_datetime(df['*DATE'])
#         df.columns = df.columns.str.replace("[OIL_RATE]", "*rOIL")
        df = df.rename(columns={'*OIL_RATE': '*rOIL'})
        df = df.rename(columns={'*WAT_RATE': '*WATER'})
        df = df.rename(columns={'*WHP': '*WHP_AVG_P'})
        df = df.rename(columns={'*WHT': '*WHT_AVG_P'})
        return df
    
    if datatype == 'month' or datatype == 'monthly':
        print('***********Accepted month data***********')
        re_writer(file_location)
        df = pd.read_csv(file_location, header=0, sep=' ', engine='python', skiprows=2, index_col=False)
        df.drop(['Unnamed: 24'], axis=1, inplace=True)
        df['*DATE'] = pd.to_datetime(df['*DATE'])
        df = df.rename(columns={'*GAS': '*rGAS'})
        df = df.rename(columns={'*WHP_P': '*WHP_AVG_P'})
        df = df.rename(columns={'*WHT_P': '*WHT_AVG_P'})

        return df
    
    if datatype == 'daily' or datatype == 'day':
        print('***********Accepted day data***********')
        re_writer(file_location)
        df = pd.read_csv(file_location, header=0, sep=' ', engine='python', skiprows=2, index_col=False)
        df.drop(['Unnamed: 28'], axis=1, inplace=True)
        df.drop(['*COND', '*DHP', '*DHT', '*AVG_CHOKE_UOM'], axis=1, inplace=True)
        df['*DATE'] = pd.to_datetime(df['*DATE'])
        df = df.rename(columns={'*GAS': '*rGAS'})
        df = df.rename(columns={'*OIL': '*rOIL'})

        return df
    
def df_lister(df, id_col, date):
    dict_ids = df[id_col].unique().tolist()
    list_ids = []
    for i in range(len(dict_ids)):
        list_ids.append(str(dict_ids[i])) # keep str values
    # create list of DataFrames
    df_list = [df.where(df[id_col] == x) for x in list_ids]
    for i in range(len(df_list)):
        df_list[i] = df_list[i].dropna(subset=[id_col])
        df_list[i] = df_list[i].sort_values([date])
    return df_list, list_ids

def dynamic_filter(df, bin_size, col_name, r_lim): # try different spread for day and month
    dfilter = df.copy()
    for row in range(1, len(df)-1):
        cur = df.loc[row, col_name] # current value
        if cur == np.nan:
            continue

        # calculate past and futur means
        if row < bin_size:
            past = df.iloc[0:row,:].loc[:, col_name]
            fut = df.iloc[row+1:row+bin_size,:].loc[:, col_name]
            m_past = past.mean()
            m_fut = fut.mean()
        elif row > len(df)-bin_size:
            past = df.iloc[row-bin_size:row,:].loc[:, col_name]
            fut = df.iloc[row+1:len(df),:].loc[:, col_name]
            m_past = past.mean()
            m_fut = fut.mean()
        else:
            past = df.iloc[row-bin_size:row,:].loc[:, col_name]
            fut = df.iloc[row+1:row+bin_size,:].loc[:, col_name]
            m_past = past.mean()
            m_fut = fut.mean()
        
        #proportion of nan in past and fut? think about this
        
        # filter if nan
        if m_past == np.nan: # can change the default value
            if abs(cur-m_fut) > r_lim:
                dfilter.loc[row, col_name] = m_fut
                continue
            else:
                continue

        if m_fut == np.nan:
            if abs(cur-m_past) > r_lim:
                dfilter.loc[row, col_name] = m_past
                continue
            else:
                continue

        # now compare means to current value
        if abs(cur-m_past) < r_lim or abs(cur-m_fut) < r_lim:
            continue
        else:
            # look at m_diff
            m_array = np.array([m_past, m_fut])
            tmp = np.isnan(m_array) # np.isnan because bin may contain nan
            m_array[tmp] = 0.0
            m_diff = abs(np.diff(m_array))[0]
#             m_diff = abs(m_past - m_fut)
            if m_diff < r_lim:
                b_mean = np.nanmean(m_array)
#                 b_mean = (m_past + m_fut)/2
                if abs(cur-b_mean) > r_lim:
                    dfilter.loc[row, col_name] = b_mean
                    continue
                else:
                    continue
            else: # check choppy bins
                max_past = past.max()
                min_past = past.min()
                max_fut = fut.max()
                min_fut = fut.min()
                if max_fut - min_fut > r_lim*2:
                    dfilter.loc[row, col_name] = m_past
                    continue
                if max_past - min_past > r_lim*2:
                    dfilter.loc[row, col_name] = m_fut
                    continue
    return dfilter

# process and split data
def clear_exc(df_list):
# remove exceptional data
    for df in df_list:
        df.loc[df['*WHP_AVG_P'] < 50, '*WHP_AVG_P'] = np.nan
        df.loc[df['*WHT_AVG_P'] < 20, '*WHT_AVG_P'] = np.nan
        df.loc[df['*BHP_AVG'] < 20, '*BHP_AVG'] = np.nan
        df.loc[df['*BHT_AVG'] < 20, '*BHT_AVG'] = np.nan
        df.loc[df['*WHP_AVG_P'] > 400, '*WHP_AVG_P'] = np.nan
        df.loc[df['*WHT_AVG_P'] > 200, '*WHT_AVG_P'] = np.nan
        df.loc[df['*BHP_AVG'] > 400, '*BHP_AVG'] = np.nan
        df.loc[df['*BHT_AVG'] > 200, '*BHT_AVG'] = np.nan
    
def process(test_list, month_list, day_list, smooth=False):
    for i in range(len(test_list)):
        test_list[i] = test_list[i].sort_values('*DATE')

    for i in range(len(month_list)):
        month_list[i] = month_list[i].sort_values('*DATE').reset_index()
        day_list[i] = day_list[i].sort_values('*DATE').reset_index()

        month_list[i]['days_in_month'] = month_list[i]['*DATE'].dt.daysinmonth
        month_list[i] = month_list[i].rename(columns={'*rOIL': '*OIL_ACCUM', '*rGAS': '*GAS_ACCUM',
                                                        '*WATER': '*WAT_ACCUM'})
        month_list[i]['*rOIL'] = month_list[i]['*OIL_ACCUM']/month_list[i]['days_in_month']
        month_list[i]['*rGAS'] = month_list[i]['*GAS_ACCUM']/month_list[i]['days_in_month']
        month_list[i]['*WATER'] = month_list[i]['*WAT_ACCUM']/month_list[i]['days_in_month']

        if smooth:
            month_list[i] = dynamic_filter(month_list[i], 30, '*BHP_AVG', 10)
            month_list[i] = dynamic_filter(month_list[i], 10, '*BHT_AVG', 50)
            month_list[i] = dynamic_filter(month_list[i], 10, '*WHP_AVG_P', 50)
            month_list[i] = dynamic_filter(month_list[i], 10, '*WHT_AVG_P', 50)

            day_list[i] = dynamic_filter(day_list[i], 30, '*BHP_AVG', 10)
            day_list[i] = dynamic_filter(day_list[i], 10, '*BHT_AVG', 50)
            day_list[i] = dynamic_filter(day_list[i], 10, '*WHP_AVG_P', 50)
            day_list[i] = dynamic_filter(day_list[i], 10, '*WHT_AVG_P', 50)   

def make_stack(test_list, month_list, day_list, well_test_ids, other_ids): 
    # restack data and prepare for plotting
    index = []
    day_bore = []
    month_bore = []
    pdf_day = []
    pdf_month = []
    test_copies = []
    cnt = 0
    for n in range(len(well_test_ids)):
        index.append([index for index, name in enumerate(other_ids) if well_test_ids[n] in name]) # get index of test_wells
        # stack dataframes for each well
        day_bore.append([day_list[index[n][i]] for i in range(len(index[n]))])
        month_bore.append([month_list[index[n][i]] for i in range(len(index[n]))])
        day_bore[n] = pd.concat(day_bore[n], ignore_index=True)
        month_bore[n] = pd.concat(month_bore[n], ignore_index=True)
        # expand test data for plotting, add well bore names 
        tmp = []
        test_list[n]['*WELL_BORE_CODE'] = other_ids[cnt]
        cnt += 1
        tmp.append(test_list[n])
        for k in range(len(index[n])-1):
            tmp_df = test_list[n].copy()
            tmp_df['*WELL_BORE_CODE'] = other_ids[cnt]
            tmp.append(tmp_df)
            cnt += 1
        test_copies.append(tmp)
        test_copies[n] = pd.concat(test_copies[n], ignore_index=True)
    # stack wells together for plotting
    all_day_bore = pd.concat(day_bore, ignore_index=True)
    all_month_bore = pd.concat(month_bore, ignore_index=True)
    expanded_test = pd.concat(test_copies, ignore_index=True)
    
    return all_day_bore, all_month_bore, expanded_test, index

def find_well(well_name, day_list, month_list, test_list, well_test_ids, well_day_ids):
    '''
    Find dataframes of wanted well
    '''
    day = []
    month = []
    test = []
    index = []
    for n in range(len(well_test_ids)):
        index = [index for index, name in enumerate(well_day_ids) if well_name in name]
    day.append([day_list[i] for i in index])
    month.append([month_list[i] for i in index])
    for n in range(len(well_test_ids)):
        index = [index for index, name in enumerate(well_test_ids) if well_name in name]
    test.append([test_list[i] for i in index])
    day = flatten(day)
    month = flatten(month)
    test = flatten(test)
    return day, month, test

def high_freq():
    # high frequency data

    # File location and type
    # file_location = "./test_pressures.xlsx"
    file_location = "../Data/General/HYME_PRESSURE_DATA/downhole pressures and oil rates c-2 h per dec 18 2013xlsx.xlsx"

    xls = pd.ExcelFile(file_location)

    df_high = []
    df_high.append(pd.read_excel(xls, 'C-2 AY1H pressure'))
    df_high.append(pd.read_excel(xls, 'C-2 AY2H pressure'))
    df_high.append(pd.read_excel(xls, 'C-2 H pressure'))
    df_high.append(pd.read_excel(xls, 'Oil rate'))
    df_high.append(pd.read_excel(xls, 'C-2 AY1H oil rate'))
    df_high.append(pd.read_excel(xls, 'C-2 AY2H oil rate'))

    C2_well = ['NO_6407/8-C-2_AY1H','NO_6407/8-C-2_AY2H','NO_6407/8-C-2_H']
    C2_bore = ['AY1H','AY2H','H']

    # trim excel data 
    df_high[0] = df_high[0][['Date', 'Pressure']]
    df_high[1] = df_high[1][['Date', 'Pressure']]
    df_high[2] = df_high[2][['Date', 'Pressure']]
    df_high[3] = df_high[3][['Date', 'OIL']]
    df_high[4] = df_high[4][['Time @ end', 'Cumulative Volume']]
    df_high[5] = df_high[5][['Time @ end', 'Cumulative Volume']]

    df_high[4] = df_high[4].rename(columns={'Time @ end': '*DATE'})
    df_high[4]['*WELL_BORE_CODE'] = C2_well[0]
    df_high[5] = df_high[5].rename(columns={'Time @ end': '*DATE'})
    df_high[5]['*WELL_BORE_CODE'] = C2_well[1]

    for i in range(3):
        df_high[i] = df_high[i].rename(columns={'Date': '*DATE', 'Pressure': '*DHP'})
        df_high[i]['*WELL_BORE_CODE'] = C2_well[i]
    df_high[3] = df_high[3].rename(columns={'Date': '*DATE', 'OIL': '*rOIL'})
    # pyo.init_notebook_mode()
    # remove unit cells
    for i in range(6):
        df_high[i].drop(df_high[i].tail(1).index, inplace=True)
        df_high[i].drop(df_high[i].head(1).index, inplace=True)
        df_high[i] = df_high[i].sort_values('*DATE', ascending=True)

    df_high[4].loc[1, '*rOIL'] = df_high[4].loc[1, 'Cumulative Volume']
    df_high[5].loc[1, '*rOIL'] = df_high[5].loc[1, 'Cumulative Volume']

    for i in range(2, len(df_high[4])):
        df_high[4].loc[i, '*rOIL'] = df_high[4].loc[i, 'Cumulative Volume'] - df_high[4].loc[i-1, 'Cumulative Volume']
        df_high[5].loc[i, '*rOIL'] = df_high[5].loc[i, 'Cumulative Volume'] - df_high[5].loc[i-1, 'Cumulative Volume']
        
    for i in range(3):
        df_high[i]['*DHP'] = pd.to_numeric(df_high[i]['*DHP']) # spark importing as string due to unit
    df_high[3]['*rOIL'] = pd.to_numeric(df_high[3]['*rOIL'])
    
    # fuse df_high together
    high_freq_p = pd.concat([df_high[0], df_high[1], df_high[2]], ignore_index=True)
    high_freq_oil = pd.concat([df_high[4], df_high[5]], ignore_index=True)

    # set up dataframe to plot with other data
    file_day = '../Data/General/HYME_DAILY_PRODUCTION/NJORD_OFM_HIST3_DAY_20131113_143735.dat'
    df_day = make_df(file_day, 'daily').sort_values('*WELL_BORE_CODE')
    day_list, well_day_ids = df_lister(df_day, '*WELL_BORE_CODE', '*DATE')
    t = np.array(well_day_ids)
    tmp = pd.DataFrame()
    tmp['*WELL_BORE_CODE'] = t
    high_freq_p = pd.concat([high_freq_p, tmp], axis=0).sort_values('*WELL_BORE_CODE')
    high_freq_oil = pd.concat([high_freq_oil, tmp], axis=0).sort_values('*WELL_BORE_CODE')
    
    # change name for clarity
    for i in range(3):
        df_high[i] = df_high[i].rename(columns={'*DHP': '*DHP '+ C2_bore[i]})
        
    return high_freq_p, high_freq_oil, df_high

# plotly of high frequency data
def h_plotly(df_high):
    C2_bore = ['AY1H','AY2H','H']
    hf_fig = make_subplots(specs=[[{"secondary_y": True}]])
    hf_fig.update_layout(
        autosize=False,
        width=1600,
        height=800,)
    for i in range(3):
        hf_fig.add_trace(go.Scattergl(x=df_high[i]['*DATE'], y=df_high[i]['*DHP '+C2_bore[i]], name=C2_bore[i], mode='markers'))
    # fig.add_trace(go.Scattergl(x=df_high[3]['*DATE'], y=df_high[3]['OIL'], name='Oil Rate', mode='lines+markers', marker_color='black'),secondary_y=True)
    hf_fig.add_trace(go.Scattergl(x=df_high[4]['*DATE'], y=df_high[4]['*rOIL'], name='AY1H oil', mode='markers'),secondary_y=True)
    hf_fig.add_trace(go.Scattergl(x=df_high[5]['*DATE'], y=df_high[5]['*rOIL'], name='AY2H oil', mode='markers'),secondary_y=True)
    hf_fig.show()

def data_plot(df_day, df_month, df_test, x_val ,y_val, title, day='Day', month='Month', test='Test'):
    day_plot = df_day.hvplot.scatter(x=x_val, y=y_val, groupby=code, height=600, width=1000, label=day, title=title)
    month_plot = df_month.hvplot.scatter(x=x_val, y=y_val, groupby=code, label=month)
    test_plot = df_test.hvplot.scatter(x=x_val, y=y_val, groupby=code, label=test)
    plot = day_plot * month_plot * test_plot
    return plot

def holo_plot(df_day, df_month, df_test):
    # oil graph
    oil = data_plot(df_day, df_month, df_test, date, oil_rate, 'OIL').opts(ylabel='Oil Rate (m\u00b3/day)')

    # gas graph
    gas = data_plot(df_day, df_month, df_test, date, gas_rate, 'GAS').opts(ylabel='Gas Rate (m\u00b3/day)')

    # water graph
    water = data_plot(df_day, df_month, df_test, date, water_rate, 'WATER').opts(ylabel='Water Rate (m\u00b3/day)')

    # pressure
    back_pressure = data_plot(df_day, df_month, df_test, date, BHP, 'Pressure', day='Day BHP', month='Month BHP', test='Test BHP')
    work_pressure = data_plot(df_day, df_month, df_test, date, WHP, 'Pressure', day='Day WHP', month='Month WHP', test='Test WHP')
    pressure = back_pressure * work_pressure
    pressure = pressure.opts(ylabel='Pressure (bar)')

    # temperature
    back_temp = data_plot(df_day, df_month, df_test, date, BHT, 'Temperature', day='Day BHT', month='Month BHT', test='Test BHT')
    work_temp = data_plot(df_day, df_month, df_test, date, WHT, 'Temperature', day='Day WHT', month='Month WHT', test='Test WHT')
    temp = back_temp * work_temp
    temp = temp.opts(ylabel='Temperature (\N{DEGREE SIGN}C)')

    return (oil + gas + water + pressure + temp).cols(2)

def plot_high_freq(df_day, df_month, df_test):
    
    
    # oil graph
    oil = data_plot(df_day, df_month, df_test, date, oil_rate, 'OIL').opts(ylabel='Oil Rate (m\u00b3/day)')

    # gas graph
    gas = data_plot(df_day, df_month, df_test, date, gas_rate, 'GAS').opts(ylabel='Gas Rate (m\u00b3/day)')

    # water graph
    water = data_plot(df_day, df_month, df_test, date, water_rate, 'WATER').opts(ylabel='Water Rate (m\u00b3/day)')

    # pressure
    back_pressure = data_plot(df_day, df_month, df_test, date, BHP, 'Pressure', day='Day BHP', month='Month BHP', test='Test BHP')
    work_pressure = data_plot(df_day, df_month, df_test, date, WHP, 'Pressure', day='Day WHP', month='Month WHP', test='Test WHP')
    pressure = back_pressure * work_pressure
    pressure = pressure.opts(ylabel='Pressure (bar)')

    # temperature
    back_temp = data_plot(df_day, df_month, df_test, date, BHT, 'Temperature', day='Day BHT', month='Month BHT', test='Test BHT')
    work_temp = data_plot(df_day, df_month, df_test, date, WHT, 'Temperature', day='Day WHT', month='Month WHT', test='Test WHT')
    temp = back_temp * work_temp
    temp = temp.opts(ylabel='Temperature (\N{DEGREE SIGN}C)')
    
    # high frequency plots
    high_freq_p, high_freq_oil, tmp= high_freq()

    high_p = high_freq_p.hvplot.scatter(x=date, y='*DHP', groupby=code, label='high_frequency') 
    pressure = pressure*high_p
    pressure = pressure.opts(ylabel='Pressure (bar)')

    high_oil = high_freq_oil.hvplot.scatter(x=date, y='*rOIL', groupby=code, label='high_frequency')
    oil = oil*high_oil
    oil = oil.opts(ylabel='Oil Rate (m\u00b3/day)')

    return (oil + gas + water + pressure + temp).cols(2)

'''
# choose files and load data into dataframes
file_test = './Data/General/HYME_WELL_TEST/NJORD_OFM_TEST_WELL_20131113_113401.dat'
file_month = './Data/General/HYME_MONTHLY_PRODUCTION/NJORD_OFM_HIST4_MONTH_20131113_113400.dat'
file_day = './Data/General/HYME_DAILY_PRODUCTION/NJORD_OFM_HIST3_DAY_20131113_143735.dat'

df_test = make_df(file_test, 'test').sort_values('*WELL_CODE')
df_month = make_df(file_month, 'monthly').sort_values('*WELL_BORE_CODE')
df_day = make_df(file_day, 'daily').sort_values('*WELL_BORE_CODE')
df_all = [df_test, df_month, df_day]

clear_exc(df_all)

# split data by well
test_list, well_test_ids = df_lister(df_test, '*WELL_CODE', '*DATE')
month_list, well_month_ids = df_lister(df_month, '*WELL_BORE_CODE', '*DATE')
day_list, well_day_ids = df_lister(df_day, '*WELL_BORE_CODE', '*DATE')

process(test_list, month_list, day_list)

df_day, df_month, df_test, index = make_stack(test_list, month_list, day_list, well_test_ids, well_day_ids)

holo_plot(df_day, df_month, df_test)

# well_finder('C-2')

high_freq_p, high_freq_oil, df_hf = high_freq()
# h_plotly(df_hf)
plot_high_freq(df_day, df_month, df_test)
'''