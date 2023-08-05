import copy
import os.path
import pandas as pd
from scipy import interpolate
import numpy as np
# from datetime import datetime   # , date, time
import datetime
import matplotlib.pyplot as plt


class PandasTools:
    def __init__(self):
        raise RuntimeError('')

    @staticmethod
    def convert_index_from_us_to_s(dataframe):
        dataframe.index = np.array(dataframe.index.tolist()) / 10 ** 6
        dataframe.index.names = ['timestamp']
        return dataframe

    @staticmethod
    def apply_time_win(dataframe, time_win):
        if (time_win is not None) and (len(time_win) == 2):
            # df = df.loc[time_win[0] < df.index < time_win[1]]
            dataframe = dataframe.loc[time_win[0] < dataframe.index]
            dataframe = dataframe.loc[dataframe.index < time_win[1]]
        return dataframe

    @staticmethod
    def apply_time_win_strptime(dataframe, time_win):
        if (time_win is not None) and (len(time_win) == 2):
            time_win_0 = datetime.datetime.strptime(time_win[0])
            time_win_1 = datetime.datetime.strptime(time_win[0])
            # df = df.loc[time_win[0] < df.index < time_win[1]]
            dataframe = dataframe.loc[time_win_0 < dataframe.index]
            dataframe = dataframe.loc[dataframe.index < time_win_1]
        return dataframe

    @staticmethod
    def interpolate_df1_according_to_df2_index(df1, df2):
        assert isinstance(df1, pd.DataFrame)
        assert isinstance(df2, pd.DataFrame)

        t1_arr = df1.index.values
        t2_arr = df2.index.values

        new_df1 = copy.deepcopy(df2)
        new_df1.drop(columns=new_df1.columns.values, inplace=True)

        for column in df1:
            x1_arr = df1[column].values
            # x2_arr = df2[df2_col].values

            # Interpolate a 1-D function.
            #
            # x and y are arrays of values used to approximate some function
            # f: y = f(x). This class returns a function whose call method uses
            # interpolation to find the value of new points.
            interp1d_fnct = interpolate.interp1d(x=t1_arr, y=x1_arr)
            new_x1_arr = interp1d_fnct(t2_arr)

            # Make sure that both ends of x1_arr are kept the same
            new_x1_arr[0] = x1_arr[0]
            new_x1_arr[-1] = x1_arr[-1]

            new_df1[column] = new_x1_arr
            # print(column)
            # print(f'len(t1_arr) {len(t1_arr)}, len(t2_arr) {len(t2_arr)}')
            # print(f'len(x1_arr) {len(x1_arr)}, len(new_x1_arr) {len(new_x1_arr)}')

        return new_df1

    @staticmethod
    def resample(df1, df1_colname, df2, df2_colname):
        assert isinstance(df1, pd.DataFrame)
        assert isinstance(df2, pd.DataFrame)

        # print('pandas_dataframe_downsample')
        df1_microseconds = np.array([int(e * 10 ** 6) for e in df1.index.values])
        # df2_microseconds = np.array([int(e * 10 ** 6) for e in df2.index.values])

        df1_timedelta = []
        for us in df1_microseconds:
            tdelta = datetime.timedelta(microseconds=int(us))
            #                 yyyy mm dd  hh  mm  ss  us
            dtime = datetime.datetime(2000, 1, 1, 00, 00, 00, 00) + tdelta
            # df1_timedelta.append(dtime)
            tstamp = pd.Timestamp(dtime)
            df1_timedelta.append(tstamp)
        # print(df1_timedelta)
        df1.index = df1_timedelta
        df1.index.names = ['timestamp']
        print(df1)
        df1 = df1.resample("0.01S")
        print(df1)
        return

        # df1_rdict = TSTools.time_statistics(t_arr=df1_microseconds, verbose=True)
        # df2_rdict = TSTools.time_statistics(t_arr=df2_microseconds, verbose=True)
        #
        # if len(df1_microseconds) < len(df2_microseconds):
        #     df1.set_index(df1_microseconds, inplace=True)
        #     df2.set_index(df2_microseconds, inplace=True)
        #     [rt1_arr, rx1_arr] = TSTools.resample(
        #         t1_arr=df1.index.values, x1_arr=df1[df1_colname].values, t2_arr=df2.index.values,
        #         tolkey='t_dt_maxusgndev', tolval=df1_rdict['t_dt_mean']/5, verbose=True)
        #
        # if len(df1_microseconds) > len(df2_microseconds):
        #     df1.set_index(df1_microseconds, inplace=True)
        #     df2.set_index(df2_microseconds, inplace=True)
        #     [rt1_arr, rx1_arr] = TSTools.resample(
        #         t1_arr=df2.index.values, x1_arr=df2[df2_colname].values, t2_arr=df1.index.values,
        #         tolkey='t_dt_maxusgndev', tolval=df1_rdict['t_dt_mean']/5, verbose=True)
        #
        # return
