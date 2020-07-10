# Author:       Bingkun Chen(992113) Zhihang Niu(1016294)
# Description:  This is the code for Group 8.
# Written:      30/5/2020
# Last updated: 14/6/2020

import pandas as pd
import geopandas as gpd
import os
import itertools
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from shapely.ops import cascaded_union
from pyproj import CRS


class DataProcessing:

    def __init__(self):
        """
        Initialize variables, set the file path required by the project,
        open the shapefile file, and wrap it in Pandas.DataFrame format
        """
        try:
            path2013 = os.path.join(os.path.curdir,
                                    'data\\VicRoadsAccidents\\2013',
                                    '2013.shp')
            path2014 = os.path.join(os.path.curdir,
                                    'data\\VicRoadsAccidents\\2014',
                                    '2014.shp')
            path2015 = os.path.join(os.path.curdir,
                                    'data\\VicRoadsAccidents\\2015',
                                    '2015.shp')
            path2016 = os.path.join(os.path.curdir,
                                    'data\\VicRoadsAccidents\\2016',
                                    '2016.shp')
            path2017 = os.path.join(os.path.curdir,
                                    'data\\VicRoadsAccidents\\2017',
                                    '2017.shp')
            path2018 = os.path.join(os.path.curdir,
                                    'data\\VicRoadsAccidents\\2018',
                                    '2018.shp')

            self.gpd2013 = gpd.read_file(path2013)
            self.gpd2014 = gpd.read_file(path2014)
            self.gpd2015 = gpd.read_file(path2015)
            self.gpd2016 = gpd.read_file(path2016)
            self.gpd2017 = gpd.read_file(path2017)
            self.gpd2018 = gpd.read_file(path2018)

            self.pd2013 = pd.DataFrame(self.gpd2013)
            self.pd2014 = pd.DataFrame(self.gpd2014)
            self.pd2015 = pd.DataFrame(self.gpd2015)
            self.pd2016 = pd.DataFrame(self.gpd2016)
            self.pd2017 = pd.DataFrame(self.gpd2017)
            self.pd2018 = pd.DataFrame(self.gpd2018)
        except OSError:
            print('Please check the file path')

    def task1_1a(self):
        """
        Calculate the total number of accidents and the average
        in these years, and print the final result.
        """
        total_accidents = (len(self.pd2013) + len(self.pd2014)
                           + len(self.pd2015) + len(self.pd2016)
                           + len(self.pd2017) + len(self.pd2018))
        average = int(total_accidents / 6)
        print('The average number of accidents per year is '
              + str(average) + '.')

    def task1_1b(self):
        """
        Complete the task 4.1.b, calculate number and ratio of the most common
        and the second most type of accident.
        """
        res_2013 = pd.DataFrame(
            self.pd2013.groupby("ACCIDENT_1")['OBJECTID'].count())
        res_2014 = pd.DataFrame(
            self.pd2014.groupby("ACCIDENT_1")['OBJECTID'].count())
        res_2015 = pd.DataFrame(
            self.pd2015.groupby("ACCIDENT_1")['OBJECTID'].count())
        res_2016 = pd.DataFrame(
            self.pd2016.groupby("ACCIDENT_1")['OBJECTID'].count())
        res_2017 = pd.DataFrame(
            self.pd2017.groupby("ACCIDENT_1")['OBJECTID'].count())
        res_2018 = pd.DataFrame(
            self.pd2018.groupby("ACCIDENT_1")['OBJECTID'].count())

        res_2013.columns = ['2013']
        t3 = res_2013.T
        res_2014.columns = ['2014']
        t4 = res_2014.T
        res_2015.columns = ['2015']
        t5 = res_2015.T
        res_2016.columns = ['2016']
        t6 = res_2016.T
        res_2017.columns = ['2017']
        t7 = res_2017.T
        res_2018.columns = ['2018']
        t8 = res_2018.T

        res = t3.append(t4).append(t5).append(t6).append(t7).append(t8)
        res = res.fillna(0).astype(int)
        res = res.T

        final_res = res.sum(axis=1)
        total_count = final_res.sum()
        most_common_type = final_res.idxmax()
        max_num = final_res.max()
        max_ratio = (max_num / total_count) * 100

        final_res.drop([most_common_type], axis=0, inplace=True)
        second_common_type = final_res.idxmax()
        second_num = final_res.max()
        second_ratio = (second_num / total_count) * 100

        print('The most common type of accident in all the recorded years is '
              + most_common_type + '(equal to ' + '%.2f' % max_ratio
              + '% accidents), and the second most common is '
              + second_common_type + '(' + '%.2f' % second_ratio + '%).')

    def task1_2a(self):
        """
        This function collects the data to generate the form of number of
        accidents by vehicle type (rows) by year (columns).
        :return: return the table for the use of task2.1
        """

        def get_count(data_array, typename):
            temp = pd.DataFrame((data_array).value_counts())
            temp.sort_values(typename, ascending=False, inplace=True)
            count = temp.iloc[1:, 0].sum()
            return count

        bic_count2013 = get_count(self.pd2013.BICYCLIST, 'BICYCLIST')
        bic_count2014 = get_count(self.pd2014.BICYCLIST, 'BICYCLIST')
        bic_count2015 = get_count(self.pd2015.BICYCLIST, 'BICYCLIST')
        bic_count2016 = get_count(self.pd2016.BICYCLIST, 'BICYCLIST')
        bic_count2017 = get_count(self.pd2017.BICYCLIST, 'BICYCLIST')
        bic_count2018 = get_count(self.pd2018.BICYCLIST, 'BICYCLIST')

        heavy_count2013 = get_count(self.pd2013.HEAVYVEHIC, 'HEAVYVEHIC')
        heavy_count2014 = get_count(self.pd2014.HEAVYVEHIC, 'HEAVYVEHIC')
        heavy_count2015 = get_count(self.pd2015.HEAVYVEHIC, 'HEAVYVEHIC')
        heavy_count2016 = get_count(self.pd2016.HEAVYVEHIC, 'HEAVYVEHIC')
        heavy_count2017 = get_count(self.pd2017.HEAVYVEHIC, 'HEAVYVEHIC')
        heavy_count2018 = get_count(self.pd2018.HEAVYVEHIC, 'HEAVYVEHIC')

        passenger_count2013 = get_count(self.pd2013.PASSENGERV, 'PASSENGERV')
        passenger_count2014 = get_count(self.pd2014.PASSENGERV, 'PASSENGERV')
        passenger_count2015 = get_count(self.pd2015.PASSENGERV, 'PASSENGERV')
        passenger_count2016 = get_count(self.pd2016.PASSENGERV, 'PASSENGERV')
        passenger_count2017 = get_count(self.pd2017.PASSENGERV, 'PASSENGERV')
        passenger_count2018 = get_count(self.pd2018.PASSENGERV, 'PASSENGERV')

        motor_count2013 = get_count(self.pd2013.MOTORCYCLE, 'MOTORCYCLE')
        motor_count2014 = get_count(self.pd2014.MOTORCYCLE, 'MOTORCYCLE')
        motor_count2015 = get_count(self.pd2015.MOTORCYCLE, 'MOTORCYCLE')
        motor_count2016 = get_count(self.pd2016.MOTORCYCLE, 'MOTORCYCLE')
        motor_count2017 = get_count(self.pd2017.MOTORCYCLE, 'MOTORCYCLE')
        motor_count2018 = get_count(self.pd2018.MOTORCYCLE, 'MOTORCYCLE')

        public_count2013 = get_count(self.pd2013.PUBLICVEHI, 'PUBLICVEHI')
        public_count2014 = get_count(self.pd2014.PUBLICVEHI, 'PUBLICVEHI')
        public_count2015 = get_count(self.pd2015.PUBLICVEHI, 'PUBLICVEHI')
        public_count2016 = get_count(self.pd2016.PUBLICVEHI, 'PUBLICVEHI')
        public_count2017 = get_count(self.pd2017.PUBLICVEHI, 'PUBLICVEHI')
        public_count2018 = get_count(self.pd2018.PUBLICVEHI, 'PUBLICVEHI')

        tab = {'2013': {'Bicycle': bic_count2013,
                        'Motorcycle': motor_count2013,
                        'Heavyvehicle': heavy_count2013,
                        'Publicvehicle': public_count2013,
                        'Passengervehicle': passenger_count2013},
               '2014': {'Bicycle': bic_count2014,
                        'Motorcycle': motor_count2014,
                        'Heavyvehicle': heavy_count2014,
                        'Publicvehicle': public_count2014,
                        'Passengervehicle': passenger_count2014},
               '2015': {'Bicycle': bic_count2015,
                        'Motorcycle': motor_count2015,
                        'Heavyvehicle': heavy_count2015,
                        'Publicvehicle': public_count2015,
                        'Passengervehicle': passenger_count2015},
               '2016': {'Bicycle': bic_count2016,
                        'Motorcycle': motor_count2016,
                        'Heavyvehicle': heavy_count2016,
                        'Publicvehicle': public_count2016,
                        'Passengervehicle': passenger_count2016},
               '2017': {'Bicycle': bic_count2017,
                        'Motorcycle': motor_count2017,
                        'Heavyvehicle': heavy_count2017,
                        'Publicvehicle': public_count2017,
                        'Passengervehicle': passenger_count2017},
               '2018': {'Bicycle': bic_count2018,
                        'Motorcycle': motor_count2018,
                        'Heavyvehicle': heavy_count2018,
                        'Publicvehicle': public_count2018,
                        'Passengervehicle': passenger_count2018}}

        tab = pd.DataFrame(tab)
        tab.sort_values(by='2013', ascending=True, inplace=True)

        latex_tab = tab.copy()
        latex_tab.index.set_names('\\diagbox{$Type$}{$Year$}', inplace=True)
        latex_tab_reset = latex_tab.reset_index()
        latex = latex_tab_reset.to_latex(column_format='lcccccc', escape=False,
                                         caption='Number of accidents by '
                                                 'vehicle type by year',
                                         label='Table 1', index=False)
        print(latex)

        return tab

    def task1_2b(self):
        """
        This function is arranged in reverse order according to the number of
        accidents in each LGA area in 2013, taking out the top 10 LGA and
        counting the data from 2014 to 2018 and calculating the difference
        and the change ratio,finally import as latex format.
        :return: return the table for the use of task2.1
        """
        temp = \
            pd.DataFrame(self.pd2013.groupby('LGA_NAME')['OBJECTID'].count())
        temp.sort_values("OBJECTID", ascending=False, inplace=True)
        temp2013 = temp.iloc[0:10, :]

        temp2014 = \
            pd.DataFrame(self.pd2014.groupby('LGA_NAME')['OBJECTID'].count())
        temp2014.sort_values("OBJECTID", ascending=False, inplace=True)
        tab = pd.merge(temp2013, temp2014, on="LGA_NAME")
        tab.columns = ['2013', '2014']
        tab['2014diff'] = tab['2014'] - tab['2013']
        tab['2014change'] = \
            (tab['2014diff'] / tab['2013']).apply(
                lambda x: '%.2f' % (x * 100)) + '\\%'

        temp2015 = \
            pd.DataFrame(self.pd2015.groupby('LGA_NAME')['OBJECTID'].count())
        temp2015.sort_values("OBJECTID", ascending=False, inplace=True)
        tab = pd.merge(tab, temp2015, on="LGA_NAME")
        tab.rename(columns={'OBJECTID': '2015'}, inplace=True)
        tab['2015diff'] = tab['2015'] - tab['2014']
        tab['2015change'] = \
            (tab['2015diff'] / tab['2014']).apply(
                lambda x: '%.2f' % (x * 100)) + '\\%'

        temp2016 = \
            pd.DataFrame(self.pd2016.groupby('LGA_NAME')['OBJECTID'].count())
        temp2016.sort_values("OBJECTID", ascending=False, inplace=True)
        tab = pd.merge(tab, temp2016, on="LGA_NAME")
        tab.rename(columns={'OBJECTID': '2016'}, inplace=True)
        tab['2016diff'] = tab['2016'] - tab['2015']
        tab['2016change'] = \
            (tab['2016diff'] / tab['2015']).apply(
                lambda x: '%.2f' % (x * 100)) + '\\%'

        temp2017 = pd.DataFrame(
            self.pd2017.groupby('LGA_NAME')['OBJECTID'].count())
        temp2017.sort_values("OBJECTID", ascending=False, inplace=True)
        tab = pd.merge(tab, temp2017, on="LGA_NAME")
        tab.rename(columns={'OBJECTID': '2017'}, inplace=True)
        tab['2017diff'] = tab['2017'] - tab['2016']
        tab['2017change'] = (tab['2017diff'] / tab['2016']).apply(
            lambda x: '%.2f' % (x * 100)) + '\\%'

        temp2018 = pd.DataFrame(
            self.pd2018.groupby('LGA_NAME')['OBJECTID'].count())
        temp2018.sort_values("OBJECTID", ascending=False, inplace=True)
        tab = pd.merge(tab, temp2018, on="LGA_NAME")
        tab.rename(columns={'OBJECTID': '2018'}, inplace=True)
        tab['2018diff'] = tab['2018'] - tab['2017']
        tab['2018change'] = (tab['2018diff'] / tab['2017']).apply(
            lambda x: '%.2f' % (x * 100)) + '\\%'

        data_tab = tab.copy()

        # latex
        tab.columns = [['2013', '2014', '2014', '2014', '2015', '2015', '2015',
                        '2016', '2016', '2016', '2017', '2017', '2017',
                        '2018', '2018', '2018'],
                       ['$No.$', '$No.$', '$Diff.$', '$Change$', '$No.$',
                        '$Diff.$', '$Change$',
                        '$No.$', '$Diff.$', '$Change$', '$No.$', '$Diff.$',
                        '$Change$',
                        '$No.$', '$Diff.$', '$Change$']]
        tab.index.set_names('\\diagbox{$LGA$}{$Year$}', inplace=True)
        tab1 = tab.loc[:, ['2013', '2014', '2015']]
        tab1_reset = tab1.reset_index()
        latex_tab1 = tab1_reset.to_latex(
            column_format='lcccrccr',
            multicolumn=True,
            multicolumn_format='c', escape=False,
            caption='The accidents change of top 10 LGAs of 2013',
            label='Table 2',
            index=False)

        tab2 = tab.loc[:, ['2016', '2017', '2018']]
        tab2_reset = tab2.reset_index()

        latex_tab2 = tab2_reset.to_latex(
            column_format='lccrccrccr',
            multicolumn=True,
            multicolumn_format='c', escape=False,
            index=False)
        print(latex_tab1)
        print(latex_tab2)

        return data_tab

    def task1_3a(self):
        """
        This function shows a bar chart of accident numbers in 2013 and 2018
        by days of the week.

        :return:
        """

        def autolabel(rects):
            # """Attach a text label above each bar in *rects*, displaying
            # its height."""
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        temp = pd.DataFrame(
            self.pd2013.groupby('DAY_OF_WEE')['OBJECTID'].count())
        temp2 = pd.DataFrame(
            self.pd2018.groupby('DAY_OF_WEE')['OBJECTID'].count())
        temp.columns = ['count']
        temp2.columns = ['count']

        labels = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
        arr_2013 = [temp.loc['Monday']['count'],
                    temp.loc['Tuesday']['count'],
                    temp.loc['Wednesday']['count'],
                    temp.loc['Thursday']['count'],
                    temp.loc['Friday']['count'],
                    temp.loc['Saturday']['count'],
                    temp.loc['Sunday']['count']]
        arr_2018 = [temp2.loc['Monday']['count'],
                    temp2.loc['Tuesday']['count'],
                    temp2.loc['Wednesday']['count'],
                    temp2.loc['Thursday']['count'],
                    temp2.loc['Friday']['count'],
                    temp2.loc['Saturday']['count'],
                    temp2.loc['Sunday']['count']]

        x = np.arange(len(labels))  # the label locations
        width = 0.35  # the width of the bars

        plt.style.use('seaborn-whitegrid')
        fig, ax = plt.subplots(figsize=(6, 5))

        rects1 = ax.bar(x - width / 2, arr_2013, width, label='2013')
        rects2 = ax.bar(x + width / 2, arr_2018, width, label='2018')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Frequency',
                      fontsize=15,
                      fontweight='roman',
                      fontstyle='italic')

        ax.set_title('Accidents in 2013 and 2018',
                     fontsize=18, fontweight='roman', fontstyle='italic')
        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=12)
        ax.legend(fontsize=14)

        autolabel(rects1)
        autolabel(rects2)

        fig.tight_layout()
        plt.show()

    def task1_3b(self):
        """
        This function outputs the line chart of the yearly change of the total
        number of accidents from all year between 2013 and 2018, for each
        severity category.
        """
        temp1 = pd.DataFrame(
            self.pd2013.groupby('SEVERITY')['OBJECTID'].count())
        temp2 = pd.DataFrame(
            self.pd2014.groupby('SEVERITY')['OBJECTID'].count())
        temp3 = pd.DataFrame(
            self.pd2015.groupby('SEVERITY')['OBJECTID'].count())
        temp4 = pd.DataFrame(
            self.pd2016.groupby('SEVERITY')['OBJECTID'].count())
        temp5 = pd.DataFrame(
            self.pd2017.groupby('SEVERITY')['OBJECTID'].count())
        temp6 = pd.DataFrame(
            self.pd2018.groupby('SEVERITY')['OBJECTID'].count())

        temp1.columns = ['2013']
        t1 = temp1.T
        temp2.columns = ['2014']
        t2 = temp2.T
        temp3.columns = ['2015']
        t3 = temp3.T
        temp4.columns = ['2016']
        t4 = temp4.T
        temp5.columns = ['2017']
        t5 = temp5.T
        temp6.columns = ['2018']
        t6 = temp6.T
        t_all = t1.append(t2).append(t3).append(t4).append(t5).append(t6)
        t_all = t_all.fillna(0).astype(int)
        t_all = t_all.T
        t_all.index.set_names('SEVERITY', inplace=True)
        t_all = t_all.reset_index()

        plt.style.use('seaborn-whitegrid')
        xlabels = ['2013', '2014', '2015', '2016', '2017', '2018']
        num_type = len(t_all)
        markers = itertools.cycle(['o', 's', 'v', 'd'])

        fig, ax = plt.subplots(figsize=(8, 6))
        for i in range(num_type):
            line = [t_all.loc[i, '2013'], t_all.loc[i, '2014'],
                    t_all.loc[i, '2015'],
                    t_all.loc[i, '2016'], t_all.loc[i, '2017'],
                    t_all.loc[i, '2018']]
            ax.plot(xlabels, line,
                    linewidth=3,
                    marker=next(markers),
                    markersize=9,
                    label=t_all.loc[i, 'SEVERITY'])

        ax.set_ylabel('Frequency',
                      fontsize=15,
                      fontweight='roman',
                      fontstyle='italic')
        ax.set_xlabel('Year',
                      fontsize=15,
                      fontweight='roman',
                      fontstyle='italic')
        ax.set_title(
            'Number of accdients for each severity categorys between 2013 to \
             2018',
            fontsize=18,
            fontweight='roman',
            fontstyle='italic')

        x = np.arange(len(xlabels))
        ax.set_xticks(x)
        ax.set_xticklabels(xlabels, fontsize=12)
        ax.legend(fontsize=14,
                  loc='upper left',
                  bbox_to_anchor=(1.02, 0.3), borderaxespad=0.)

        plt.show()

    def task1_3c(self):
        """
         This function shows 2 sub-ﬁgures to describe showing the fraction of
         the most common category of accidents per LGA. Using Geopandas and
         suitable basemap to draw choropleth maps
        """
        temp2013 = pd.DataFrame(
            self.pd2013.groupby(['LGA_NAME', 'SEVERITY'])['OBJECTID'].count())
        temp2018 = pd.DataFrame(
            self.pd2018.groupby(['LGA_NAME', 'SEVERITY'])['OBJECTID'].count())

        temp2013.rename(columns={'OBJECTID': 'count'}, inplace=True)
        temp2013.sort_values(by=["LGA_NAME", "count"], ascending=False,
                             inplace=True)
        temp2013['rank'] = temp2013['count'].groupby("LGA_NAME").rank(
            method='first', ascending=False)
        temp2013 = temp2013.loc[temp2013['rank'] == 1.0].copy()
        tab2013 = pd.DataFrame(
            self.pd2013.groupby('LGA_NAME')['OBJECTID'].count())
        temp2013 = temp2013.merge(tab2013, on='LGA_NAME')
        temp2013['fraction'] = (100 * temp2013['count']) / temp2013['OBJECTID']
        temp13 = temp2013.reset_index()
        temp2013 = temp13.set_index('LGA_NAME')

        temp2018.rename(columns={'OBJECTID': 'count'}, inplace=True)
        temp2018.sort_values(by=["LGA_NAME", "count"], ascending=False,
                             inplace=True)
        temp2018['rank'] = temp2018['count'].groupby("LGA_NAME").rank(
            method='first', ascending=False)
        temp2018 = temp2018.loc[temp2018['rank'] == 1.0].copy()
        tab2018 = pd.DataFrame(
            self.pd2018.groupby('LGA_NAME')['OBJECTID'].count())
        temp2018 = temp2018.merge(tab2018, on='LGA_NAME')
        temp2018['fraction'] = (100 * temp2018['count']) / temp2018['OBJECTID']
        temp18 = temp2018.reset_index()
        temp2018 = temp18.set_index('LGA_NAME')

        dict2013 = temp13[['LGA_NAME', 'fraction']].set_index(
            'LGA_NAME').to_dict()
        dict2013 = dict2013['fraction']

        dict2018 = temp18[['LGA_NAME', 'fraction']].set_index(
            'LGA_NAME').to_dict()
        dict2018 = dict2018['fraction']

        arr_2013 = temp2013['fraction'].values
        arr_2018 = temp2018['fraction'].values
        values = np.append(arr_2013, arr_2018)

        # setup Lambert Conformal basemap.
        # set resolution=None to skip processing of boundary datasets.
        num_colors = 20
        cm = plt.get_cmap('Reds')
        scheme = [cm(i / num_colors) for i in range(num_colors)]
        bins = np.linspace(values.min(), values.max(), num_colors)
        temp2013['bin'] = np.digitize(arr_2013, bins) - 1
        temp2018['bin'] = np.digitize(arr_2018, bins) - 1

        fig = plt.figure(figsize=(14, 7))
        fig.tight_layout()
        ax_legend = fig.add_axes([0.122, 0.18, 0.78, 0.03], zorder=1)

        ax1 = fig.add_subplot(121)
        m = Basemap(width=12000000, height=9000000, projection='lcc',
                    resolution='f',
                    lat_0=-37.45,
                    lon_0=145.1,
                    llcrnrlon=138.8,
                    llcrnrlat=-39.74,
                    urcrnrlon=150.8,
                    urcrnrlat=-33.55)

        parallels = np.arange(-40., -30., 2.)
        m.drawparallels(parallels, labels=[False, True, True, False])
        meridians = np.arange(130., 160., 2.)
        m.drawmeridians(meridians, labels=[True, False, False, True])

        m.shadedrelief()
        m.readshapefile('add_dataset/LGA/LGA', 'country', drawbounds=False)

        for info, shape in zip(m.country_info, m.country):
            if info['LGA_NAME17'] in dict2013.keys():
                lga_name = info['LGA_NAME17']
                color = scheme[int(temp2013.loc[lga_name]['bin'])]

                patches = [Polygon(np.array(shape), True)]
                pc = PatchCollection(patches)
                pc.set_facecolor(color)
                pc.set_alpha(0.7)
                pc.set_edgecolor('#52616b')
                ax1.add_collection(pc)

            ax1.set_title('Year 2013',
                          fontsize=18,
                          fontweight='roman',
                          fontstyle='italic')

        ax2 = fig.add_subplot(122)
        m = Basemap(width=12000000, height=9000000, projection='lcc',
                    resolution='f',
                    lat_0=-37.45,
                    lon_0=145.1,
                    llcrnrlon=138.8,
                    llcrnrlat=-39.74,
                    urcrnrlon=150.8,
                    urcrnrlat=-33.55)

        parallels = np.arange(-40., -30., 2.)
        m.drawparallels(parallels, labels=[False, True, True, False])
        meridians = np.arange(130., 160., 2.)
        m.drawmeridians(meridians, labels=[True, False, False, True])

        m.shadedrelief()
        m.readshapefile('add_dataset/LGA/LGA', 'country', drawbounds=False)

        for info, shape in zip(m.country_info, m.country):
            if info['LGA_NAME17'] in dict2018.keys():
                lga_name = info['LGA_NAME17']
                color = scheme[int(temp2018.loc[lga_name]['bin'])]

                patches = [Polygon(np.array(shape), True)]
                pc = PatchCollection(patches)
                pc.set_facecolor(color)
                pc.set_alpha(0.7)
                pc.set_edgecolor('#52616b')
                ax2.add_collection(pc)

            ax2.set_title('Year 2018',
                          fontsize=18,
                          fontweight='roman',
                          fontstyle='italic')

            cmap = mpl.colors.ListedColormap(scheme)
            cb = mpl.colorbar.ColorbarBase(ax_legend, cmap=cmap, ticks=bins,
                                           boundaries=bins,
                                           orientation='horizontal')
            cb.ax.set_xticklabels([str(round(i, 1)) for i in bins])

        plt.show()

    def task2_1(self, acc_year, acc_lga):
        """
        This function writes two layer into a geopackage,the data was provided
        by Task1.2
        :param acc_year: provided by Task1.2a
        :param acc_lga: provided by Task1.2b
        """
        try:
            pa = 'add_dataset\\LGA_task2\\LGA_task2.shp'
            acc_year.reset_index(inplace=True)
            acc_lga.reset_index(inplace=True)
            lga_task = gpd.read_file(pa)
            lga_clean = lga_task.loc[lga_task.is_valid]
            vic_poly = []
            for a in range(0, len(lga_clean)):
                vic_poly.append(lga_clean.geometry.values[a])

            boundary = gpd.GeoSeries(cascaded_union(vic_poly))

            t_year = gpd.GeoDataFrame(acc_year, geometry=boundary.centroid)
            # AccidentByYear

            lga_task.rename(columns={'ABB_NAME': 'LGA_NAME'}, inplace=True)
            tab_type = pd.merge(acc_lga, lga_task, on='LGA_NAME')
            t_lga = gpd.GeoDataFrame(acc_lga, geometry=tab_type.geometry)

            t_lga.crs = CRS.from_epsg(3857).to_wkt()
            t_year.crs = CRS.from_epsg(3857).to_wkt()

            t_year.to_file("output\\Task2.gpkg", layer='AccidentsByYear',
                           driver="GPKG")
            t_lga.to_file("output\\Task2.gpkg", layer='AccidentsByLGA',
                          driver="GPKG")
        except OSError:
            print('Please check the file path')

    def task2_2(self):
        """
        This function writes a layer “AccidentLocations” into the geopackage.
        selecting accidents with at least 3 people involved,and add five fields
        """
        temp2013 = self.pd2013[self.pd2013["TOTAL_PERS"] >= 3]
        temp2014 = self.pd2014[self.pd2014["TOTAL_PERS"] >= 3]
        temp2015 = self.pd2015[self.pd2015["TOTAL_PERS"] >= 3]
        temp2016 = self.pd2016[self.pd2016["TOTAL_PERS"] >= 3]
        temp2017 = self.pd2017[self.pd2017["TOTAL_PERS"] >= 3]
        temp2018 = self.pd2018[self.pd2018["TOTAL_PERS"] >= 3]

        attri_2013 = temp2013[["OBJECTID", "ACCIDENT_N", "DAY_OF_WEE",
                               "TOTAL_PERS", "SEVERITY",
                               "LONGITUDE", "LATITUDE"]]
        attri_2014 = temp2014[["OBJECTID", "ACCIDENT_N", "DAY_OF_WEE",
                               "TOTAL_PERS", "SEVERITY",
                               "LONGITUDE", "LATITUDE"]]
        attri_2015 = temp2015[["OBJECTID", "ACCIDENT_N", "DAY_OF_WEE",
                               "TOTAL_PERS", "SEVERITY",
                               "LONGITUDE", "LATITUDE"]]
        attri_2016 = temp2016[["OBJECTID", "ACCIDENT_N", "DAY_OF_WEE",
                               "TOTAL_PERS", "SEVERITY",
                               "LONGITUDE", "LATITUDE"]]
        attri_2017 = temp2017[["OBJECTID", "ACCIDENT_N", "DAY_OF_WEE",
                               "TOTAL_PERS", "SEVERITY",
                               "LONGITUDE", "LATITUDE"]]
        attri_2018 = temp2018[["OBJECTID", "ACCIDENT_N", "DAY_OF_WEE",
                               "TOTAL_PERS", "SEVERITY",
                               "LONGITUDE", "LATITUDE"]]

        temp_tab1 = pd.concat([attri_2013, attri_2014, attri_2015,
                               attri_2016, attri_2017, attri_2018],
                              ignore_index=True)

        veh_2013 = temp2013[['OBJECTID', 'BICYCLIST',
                             'HEAVYVEHIC', 'PASSENGERV',
                             'MOTORCYCLE', 'PUBLICVEHI']]
        veh_2014 = temp2014[['OBJECTID', 'BICYCLIST',
                             'HEAVYVEHIC', 'PASSENGERV',
                             'MOTORCYCLE', 'PUBLICVEHI']]
        veh_2015 = temp2015[['OBJECTID', 'BICYCLIST',
                             'HEAVYVEHIC', 'PASSENGERV',
                             'MOTORCYCLE', 'PUBLICVEHI']]
        veh_2016 = temp2016[['OBJECTID', 'BICYCLIST',
                             'HEAVYVEHIC', 'PASSENGERV',
                             'MOTORCYCLE', 'PUBLICVEHI']]
        veh_2017 = temp2017[['OBJECTID', 'BICYCLIST',
                             'HEAVYVEHIC', 'PASSENGERV',
                             'MOTORCYCLE', 'PUBLICVEHI']]
        veh_2018 = temp2018[['OBJECTID', 'BICYCLIST',
                             'HEAVYVEHIC', 'PASSENGERV',
                             'MOTORCYCLE', 'PUBLICVEHI']]

        temp_tab2 = pd.concat([veh_2013, veh_2014, veh_2015,
                               veh_2016, veh_2017, veh_2018],
                              ignore_index=True)

        def getstring(type_a, type_b, type_c, type_d, type_e):
            empty = ''
            ve_type = ''
            if type_a + type_b + type_c + type_d + type_e > 0:
                if type_a >= 1:
                    ve_type = ve_type + str('Bicycle ')
                if type_b >= 1:
                    ve_type = ve_type + str('Heavyvehicle ')
                if type_c >= 1:
                    ve_type = ve_type + str('Motorcycle ')
                if type_d >= 1:
                    ve_type = ve_type + str('Passengervehicle ')
                if type_e >= 1:
                    ve_type = ve_type + str('Publicvehicle ')
                return ve_type
            else:
                return empty

        temp_tab2['VehicleType'] = temp_tab2.apply(
            lambda x: getstring(x.BICYCLIST,
                                x.HEAVYVEHIC,
                                x.MOTORCYCLE,
                                x.PASSENGERV,
                                x.PUBLICVEHI),
            axis=1)

        temp_tab2 = temp_tab2[['OBJECTID', 'VehicleType']]
        acc_loc = pd.merge(temp_tab2, temp_tab1, on='OBJECTID')
        acc_loc_final = acc_loc.drop(
            columns=['OBJECTID', 'LONGITUDE', 'LATITUDE'])

        acc_loc_final.rename(columns={'ACCIDENT_N': 'AccidentNumber'},
                             inplace=True)
        acc_loc_final.rename(columns={'DAY_OF_WEE': 'DayOfWeek'}, inplace=True)
        acc_loc_final.rename(columns={'TOTAL_PERS': 'NumPeople'}, inplace=True)
        acc_loc_final.rename(columns={'SEVERITY': 'Severity'}, inplace=True)

        acc_loc_final = acc_loc_final[['AccidentNumber', 'VehicleType',
                                       'DayOfWeek', 'NumPeople', 'Severity']]
        geo_acc_loc = gpd.GeoDataFrame(acc_loc_final,
                                       geometry=gpd.points_from_xy(
                                           acc_loc.LONGITUDE,
                                           acc_loc.LATITUDE))
        geo_acc_loc.crs = CRS.from_epsg(4283).to_wkt()
        geo_acc_loc.to_file("output\\Task2.gpkg",
                            layer='AccidentLocations',
                            driver="GPKG")
        return geo_acc_loc

    def task2_3_spatialJoin(self):
        """
        This function uses spatial join to achieve adding
         a new ﬁeld “SA2” to ”AccidentLocations”.
        :return:the spatial join result
        """
        try:
            gpkg_path = "output\\Task2.gpkg"
            sa2_path = "data\\RegionsSA2_2016\\SA2_2016_AUST.shp"

            # Accidentlocation points
            gpd_acc_loc = gpd.read_file(gpkg_path, layer='AccidentLocations')
            # SA2 area polygons
            gpd_sa2 = gpd.read_file(sa2_path)

            # Clear the invalid geometries
            acc_clean = gpd_acc_loc.loc[gpd_acc_loc.is_valid]
            sa2_clean = gpd_sa2.loc[gpd_sa2.is_valid]

            # Spatial join
            acc_within_sa2 = gpd.sjoin(acc_clean, sa2_clean,
                                       how="inner",
                                       op='intersects')

            temp_tab = acc_within_sa2[['AccidentNumber', 'SA2_NAME16']]
            gpd_acc_loc = gpd_acc_loc.merge(temp_tab, on='AccidentNumber')
            gpd_acc_loc.rename(columns={'SA2_NAME16': 'SA2'}, inplace=True)
            gpd_acc_loc = gpd_acc_loc[['AccidentNumber', 'VehicleType',
                                       'DayOfWeek', 'NumPeople',
                                       'Severity', 'geometry', 'SA2']]
            gpd_acc_loc.to_file("output\\Task2.gpkg",
                                layer='AccidentLocations',
                                driver="GPKG")
            return gpd_acc_loc
        except OSError:
            print('Please check the file path')

    def task2_3_withoutSpatialIndex(self):
        """
        Achieve spatial join without using spatial index,this function using
        intersects to query the relation between points and polygons
        :return: the result without spatial index
        """
        try:
            gpkg_path = "output\\Task2.gpkg"
            sa2_path = "data\\RegionsSA2_2016\\SA2_2016_AUST.shp"

            # Accidentlocation points
            gpd_acc_loc = gpd.read_file(gpkg_path, layer='AccidentLocations')
            # SA2 area polygons
            gpd_sa2 = gpd.read_file(sa2_path)

            # Clear the invalid geometries in Accidentlocation
            acc_clean = gpd_acc_loc.loc[gpd_acc_loc.is_valid]
            # Clear the invalid geometries in SA2
            sa2_clean = gpd_sa2.loc[gpd_sa2.is_valid]

            # Query without spatial index
            for index, sa2 in sa2_clean.iterrows():
                acc_clean.loc[acc_clean.intersects(sa2.geometry), 'SA2'] = sa2[
                    'SA2_NAME16']
            acc_clean = acc_clean[['AccidentNumber', 'VehicleType',
                                   'DayOfWeek', 'NumPeople',
                                   'Severity', 'geometry', 'SA2']]
            return acc_clean
        except OSError:
            print('Please check the file path')

    def task2_3_spatialIndex_Rtree(self):
        """
        This function using RTree (spatial index) to achieve spatial join,
        Select each polygon and use the R tree to establish a spatial index
        to query the internal points
        :return: the result of spatial join
        """
        try:
            gpkg_path = "output\\Task2.gpkg"
            sa2_path = "data\\RegionsSA2_2016\\SA2_2016_AUST.shp"

            # Accidentlocation points
            gpd_acc_loc = gpd.read_file(gpkg_path, layer='AccidentLocations')
            # SA2 area polygons
            gpd_sa2 = gpd.read_file(sa2_path)

            # Clear the invalid geometries in Accidentlocation
            acc_clean = gpd_acc_loc.loc[gpd_acc_loc.is_valid]
            # Clear the invalid geometries in SA2
            sa2_clean = gpd_sa2.loc[gpd_sa2.is_valid]
            # Create spatial index
            spatial_index = acc_clean.sindex

            # Implement spatial index through R-tree
            for index, sa2 in sa2_clean.iterrows():
                possible_matches_index = list(
                    spatial_index.intersection(sa2.geometry.bounds))
                possible_matches = acc_clean.iloc[possible_matches_index]
                final_selection = possible_matches[
                    possible_matches.intersects(sa2.geometry)].index
                acc_clean.loc[final_selection, 'SA2'] = sa2['SA2_NAME16']
            acc_clean = acc_clean[['AccidentNumber', 'VehicleType',
                                   'DayOfWeek', 'NumPeople',
                                   'Severity', 'geometry', 'SA2']]
            return acc_clean
        except OSError:
            print('Please check the file path')

    def task2_4(self):
        """
        Read the created layer and split the layer into two layers by weekdays
        and weekend.
        """
        try:
            gpkg_path = "output\\Task2.gpkg"
            # Accidentlocation points
            gpd_acc = gpd.read_file(gpkg_path, layer='AccidentLocations')

            weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
            weekends = ['Saturday', 'Sunday']
            severities = ['Serious injury accident', 'Fatal accident']

            acc_weekday = gpd.GeoDataFrame()
            final_acc_weekday = gpd.GeoDataFrame()

            for weekday in weekdays:
                acc_weekday = acc_weekday.append(
                    gpd_acc[gpd_acc['DayOfWeek'] == weekday])
            for severity in severities:
                final_acc_weekday = final_acc_weekday.append(
                    acc_weekday[acc_weekday['Severity'] == severity])

            acc_weekend = gpd.GeoDataFrame()
            final_acc_weekend = gpd.GeoDataFrame()

            for weekend in weekends:
                acc_weekend = acc_weekend.append(
                    gpd_acc[gpd_acc['DayOfWeek'] == weekend])
            for severity in severities:
                final_acc_weekend = final_acc_weekend.append(
                    acc_weekend[acc_weekend['Severity'] == severity])

            final_acc_weekday.to_file("output\\Task2.gpkg",
                                      layer='SevereAccidentsWeekday',
                                      driver="GPKG")

            final_acc_weekend.to_file("output\\Task2.gpkg",
                                      layer='SevereAccidentsWeekend',
                                      driver="GPKG")
        except OSError:
            print('Please check the file path')
