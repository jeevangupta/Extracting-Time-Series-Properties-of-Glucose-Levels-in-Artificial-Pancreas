#!/usr/local/bin/python3
#command to run file : $ python3 ./main.py -a ./data/CGMData.csv -b ./data/InsulinData.csv

import sys
import os.path
import getopt
import pandas as pd
import csv
from datetime import datetime, timedelta


def isFile(fileName):
    if(not os.path.isfile(fileName)):
        raise ValueError("\n *** You must provide a valid filename as parameter *** ", fileName)
 
#function to read to command line parameter.
def readfile(argv):
    global cgm_data_file
    global insulin_data_file
    cgm_data_file = "./data/CGMData.csv"
    insulin_data_file = "./data/InsulinData.csv"
    try:
        opts, args = getopt.getopt(argv,"a:b:")
    except getopt.GetoptError:
        sys.exc_info()
        
    for opt, arg in opts:
        if opt == "-a":
            cgm_data_file = arg
            isFile(cgm_data_file)
        elif opt == "-b":
            insulin_data_file = arg
            isFile(insulin_data_file)
        else:
            print("\n*** Invalid Option in command line *** ")


def get_auto_manul_data(cgm_data, auto_mode_start_date, auto_mode_start_time):
    try:
        cgm_data.rename(columns = {'Sensor Glucose (mg/dL)':'CGM'}, inplace = True)
        cgm_data['CGM'] = pd.to_numeric(cgm_data['CGM'],errors='coerce')

        cgm_data['DateTime'] = pd.to_datetime(cgm_data['Date']+" "+cgm_data['Time'],format="%m/%d/%Y %H:%M:%S")
        #print("\n CGM DATA\n",cgm_data)

        date_string = auto_mode_start_date+" "+auto_mode_start_time
        date = datetime.strptime(date_string, "%m/%d/%Y %H:%M:%S")
        #print(f"auto mode start datetime: {date}")

        auto_mode_data = cgm_data.loc[cgm_data['DateTime'] >= date]
        #auto_mode_data = auto_mode_data[~auto_mode_data['CGM'].isna()]
        #print("\n auto_mode_data :\n",auto_mode_data)

        manual_mode_data = cgm_data.loc[cgm_data['DateTime'] < date]
        #print("\n manual_mode_data :\n",manual_mode_data)

        #manual_mode_data = manual_mode_data[~manual_mode_data['CGM'].isna()]
        #print("\n manual_mode_data :\n",manual_mode_data)

        return auto_mode_data, manual_mode_data
    except:
        print("\n*** Function (get_auto_manul_data1) Failed *** ", sys.exc_info())


def extract_metrics(mode_data_df):
    try:
        cgm = ['CGM > 180','CGM > 250','CGM >= 70 and CGM <= 180','CGM >= 70 and CGM <= 150','CGM < 70','CGM < 54']
        s = ['0:0:0','06:00:00','0:00:00']
        e = ['6:00:00','24:00:00','24:00:00']

        pd.to_datetime(mode_data_df['Time'],format="%H:%M:%S")
        t = []
        for i,j in zip(s,e):
            tmp = []
            for k in cgm:
                qry = "Time >='%s' and Time<='%s' and %s" %(i,j,k)
                val = calculate_perc(mode_data_df,qry)
                tmp.append(round(val,2))
            t.extend(tmp)

        return t
    except:
        print("\n*** Function (extract_metrics) Failed *** ", sys.exc_info())


def calculate_perc(data_df,qry):
    try:
        dt = data_df.query(qry)
        dt = dt.groupby('Date').size().reset_index(name='count')
        #print(dt.head())

        #dt['perc'] =  round(dt['count'] / 288 *100,2)

        dt['perc'] =  dt['count'] / 288 *100
        dt_val = dt['perc'].mean()

        return dt_val
    except:
        print("\n*** Function (calculate_perc) Failed *** ", sys.exc_info())


def delete_nan_record_day(df):
    try:
        na_df = df[df['CGM'].isna()]
        na_df = na_df.groupby('Date').size().reset_index(name='count')

        na_df['perc'] =  round(na_df['count'] / 288 *100)
        na_df = na_df[na_df['perc'] >= 42.5]
        nan_date_list = na_df['Date'].tolist()

        #df = df.groupby('Date').size().reset_index(name='count')
        df = df[~df['Date'].isin(nan_date_list)]

        return df
    except:
        print("\n*** Function (delete_nan_record_day) Failed *** ",sys.exc_info())


if __name__ == '__main__':
    try:
        timestamp = datetime.strftime(datetime.now(),'%Y-%m-%d')
        print("DATE : ",timestamp)
        print("Extracting Time Series Properties of Glucose Levels in Artificial Pancreas.")
        readfile(sys.argv[1:])

        cgm_data = pd.read_csv(cgm_data_file, usecols=['Date','Time','Sensor Glucose (mg/dL)','ISIG Value'])
        insulin_data = pd.read_csv(insulin_data_file, usecols=['Date','Time','Alarm'])

        #determine when auto mode start
        auto_mode_start = insulin_data[insulin_data['Alarm'] == 'AUTO MODE ACTIVE PLGM OFF'].iloc[-1]
        #print("\n ",auto_mode_start)
        auto_mode_start_time = auto_mode_start['Time']
        auto_mode_start_date = auto_mode_start['Date']
        print(f"\n auto_mode_start_date : {auto_mode_start_date} \n auto_mode_start_time : {auto_mode_start_time}")

        auto_mode_data, manual_mode_data = get_auto_manul_data(cgm_data, auto_mode_start_date, auto_mode_start_time)
        
        manual_mode_data = delete_nan_record_day(manual_mode_data)
        manual_val_list = extract_metrics(manual_mode_data)
        

        auto_mode_data = delete_nan_record_day(auto_mode_data)
        auto_val_list = extract_metrics(auto_mode_data)
        
        cgm = ['CGM > 180','CGM > 250','CGM >= 70 and CGM <= 180','CGM >= 70 and CGM <= 150','CGM < 70','CGM < 54']
        manual_metric_data = dict(zip(cgm, manual_val_list))
        print(f"\n Manual mode metric data: \n {manual_metric_data}")
        
        auto_metric_data = dict(zip(cgm, manual_val_list))
        print(f"\n Auto mode metric data: \n {auto_metric_data}")

    except:
        print("\n*** Extracting Time Series Properties of Glucose Levels in Artificial Pancreas Processing Failed *** ", sys.exc_info())


