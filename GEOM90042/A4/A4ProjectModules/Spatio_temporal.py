# Author:       Bingkun Chen(992113) Zhihang Niu(1016294)
# Description:  This is the code for Group 8.
# Written:      30/5/2020
# Last updated: 14/6/2020

import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import geopandas as gpd
import plotly as py
import os
import numpy as np
import json
from pyproj import CRS


class Spatio_temporal:

    def __init__(self):
        """
        Initialize variables, set the file path required by the project, open
        the shapefile file, and wrap it in Pandas.DataFrame format
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
            path_acc = os.path.join(os.path.curdir,
                                    'data\\RegionsSA2_2016',
                                    'SA2_2016_AUST.shp')

            self.gpd2013 = gpd.read_file(path2013)
            self.gpd2014 = gpd.read_file(path2014)
            self.gpd2015 = gpd.read_file(path2015)
            self.gpd2016 = gpd.read_file(path2016)
            self.gpd2017 = gpd.read_file(path2017)
            self.gpd2018 = gpd.read_file(path2018)
            self.gpd_acc = gpd.read_file(path_acc)

            self.pd2013 = pd.DataFrame(self.gpd2013)
            self.pd2014 = pd.DataFrame(self.gpd2014)
            self.pd2015 = pd.DataFrame(self.gpd2015)
            self.pd2016 = pd.DataFrame(self.gpd2016)
            self.pd2017 = pd.DataFrame(self.gpd2017)
            self.pd2018 = pd.DataFrame(self.gpd2018)
        except OSError:
            print('Please check the file path')

    def datapreparation(self):
        """
        This function is used to data preprocessing in task3
        :return: preprocessed the data using in the following analysis
        """

        temp2013 = self.pd2013[
            ["ACCIDENT_N", "ACCIDENT_D", "ACCIDENT_1", "DAY_OF_WEE",
             "TOTAL_PERS", "SEVERITY", "ALCOHOL_RE", "UNLICENCSE",
             "LONGITUDE", "LATITUDE", "PED_CYCLIS", "PED_CYCL_1", "OLD_PEDEST",
             "OLD_DRIVER", "YOUNG_DRIV"]]
        temp2014 = self.pd2014[
            ["ACCIDENT_N", "ACCIDENT_D", "ACCIDENT_1", "DAY_OF_WEE",
             "TOTAL_PERS", "SEVERITY", "ALCOHOL_RE", "UNLICENCSE",
             "LONGITUDE", "LATITUDE", "PED_CYCLIS", "PED_CYCL_1", "OLD_PEDEST",
             "OLD_DRIVER", "YOUNG_DRIV"]]
        temp2015 = self.pd2015[
            ["ACCIDENT_N", "ACCIDENT_D", "ACCIDENT_1", "DAY_OF_WEE",
             "TOTAL_PERS", "SEVERITY", "ALCOHOL_RE", "UNLICENCSE",
             "LONGITUDE", "LATITUDE", "PED_CYCLIS", "PED_CYCL_1", "OLD_PEDEST",
             "OLD_DRIVER", "YOUNG_DRIV"]]
        temp2016 = self.pd2016[
            ["ACCIDENT_N", "ACCIDENT_D", "ACCIDENT_1", "DAY_OF_WEE",
             "TOTAL_PERS", "SEVERITY", "ALCOHOL_RE", "UNLICENCSE",
             "LONGITUDE", "LATITUDE", "PED_CYCLIS", "PED_CYCL_1", "OLD_PEDEST",
             "OLD_DRIVER", "YOUNG_DRIV"]]
        temp2017 = self.pd2017[
            ["ACCIDENT_N", "ACCIDENT_D", "ACCIDENT_1", "DAY_OF_WEE",
             "TOTAL_PERS", "SEVERITY", "ALCOHOL_RE", "UNLICENCSE",
             "LONGITUDE", "LATITUDE", "PED_CYCLIS", "PED_CYCL_1", "OLD_PEDEST",
             "OLD_DRIVER", "YOUNG_DRIV"]]
        temp2018 = self.pd2018[
            ["ACCIDENT_N", "ACCIDENT_D", "ACCIDENT_1", "DAY_OF_WEE",
             "TOTAL_PERS", "SEVERITY", "ALCOHOL_RE", "UNLICENCSE",
             "LONGITUDE", "LATITUDE", "PED_CYCLIS", "PED_CYCL_1", "OLD_PEDEST",
             "OLD_DRIVER", "YOUNG_DRIV"]]

        acc_clean = self.gpd_acc.loc[self.gpd_acc.is_valid]

        geo2013 = gpd.GeoDataFrame(temp2013, geometry=gpd.points_from_xy(
            temp2013.LONGITUDE, temp2013.LATITUDE))
        geo2014 = gpd.GeoDataFrame(temp2014, geometry=gpd.points_from_xy(
            temp2014.LONGITUDE, temp2014.LATITUDE))
        geo2015 = gpd.GeoDataFrame(temp2015, geometry=gpd.points_from_xy(
            temp2015.LONGITUDE, temp2015.LATITUDE))
        geo2016 = gpd.GeoDataFrame(temp2016, geometry=gpd.points_from_xy(
            temp2016.LONGITUDE, temp2016.LATITUDE))
        geo2017 = gpd.GeoDataFrame(temp2017, geometry=gpd.points_from_xy(
            temp2017.LONGITUDE, temp2017.LATITUDE))
        geo2018 = gpd.GeoDataFrame(temp2018, geometry=gpd.points_from_xy(
            temp2018.LONGITUDE, temp2018.LATITUDE))

        geo2013.crs = CRS.from_epsg(4283).to_wkt()
        geo2014.crs = CRS.from_epsg(4283).to_wkt()
        geo2015.crs = CRS.from_epsg(4283).to_wkt()
        geo2016.crs = CRS.from_epsg(4283).to_wkt()
        geo2017.crs = CRS.from_epsg(4283).to_wkt()
        geo2018.crs = CRS.from_epsg(4283).to_wkt()

        ac_sa2013 = gpd.sjoin(geo2013, acc_clean, how="inner", op='intersects')
        ac_sa2014 = gpd.sjoin(geo2014, acc_clean, how="inner", op='intersects')
        ac_sa2015 = gpd.sjoin(geo2015, acc_clean, how="inner", op='intersects')
        ac_sa2016 = gpd.sjoin(geo2016, acc_clean, how="inner", op='intersects')
        ac_sa2017 = gpd.sjoin(geo2017, acc_clean, how="inner", op='intersects')
        ac_sa2018 = gpd.sjoin(geo2018, acc_clean, how="inner", op='intersects')

        tab2013 = ac_sa2013[["SA2_NAME16", "ACCIDENT_N"]]
        gcc_2013 = geo2013.merge(tab2013, on="ACCIDENT_N")
        gcc_2013 = gcc_2013.drop(columns=['LONGITUDE', 'LATITUDE'])

        tab2014 = ac_sa2014[["SA2_NAME16", "ACCIDENT_N"]]
        gcc_2014 = geo2014.merge(tab2014, on="ACCIDENT_N")
        gcc_2014 = gcc_2014.drop(columns=['LONGITUDE', 'LATITUDE'])

        tab2015 = ac_sa2015[["SA2_NAME16", "ACCIDENT_N"]]
        gcc_2015 = geo2015.merge(tab2015, on="ACCIDENT_N")
        gcc_2015 = gcc_2015.drop(columns=['LONGITUDE', 'LATITUDE'])

        tab2016 = ac_sa2016[["SA2_NAME16", "ACCIDENT_N"]]
        gcc_2016 = geo2016.merge(tab2016, on="ACCIDENT_N")
        gcc_2016 = gcc_2016.drop(columns=['LONGITUDE', 'LATITUDE'])

        tab2017 = ac_sa2017[["SA2_NAME16", "ACCIDENT_N"]]
        gcc_2017 = geo2017.merge(tab2017, on="ACCIDENT_N")
        gcc_2017 = gcc_2017.drop(columns=['LONGITUDE', 'LATITUDE'])

        tab2018 = ac_sa2018[["SA2_NAME16", "ACCIDENT_N"]]
        gcc_2018 = geo2018.merge(tab2018, on="ACCIDENT_N")
        gcc_2018 = gcc_2018.drop(columns=['LONGITUDE', 'LATITUDE'])

        tab = pd.concat(
            [gcc_2013, gcc_2014, gcc_2015, gcc_2016, gcc_2017, gcc_2018],
            ignore_index=True)
        tab['year'] = pd.to_datetime(tab['ACCIDENT_D']).dt.year

        return tab

    def acc_map(self, pd_all):
        """
        This function outputs choropleth map to illustrate the distribution
         of accidents between 2013 to 2018
         :output: save the choropleth map with timescale as a HTML format
        """
        try:
            pd_select = pd_all.groupby(['year', 'SA2_NAME16'])[
                'ACCIDENT_N'].count()
            pd_allyear = pd_select.reset_index()
            with open("add_dataset\\Vic.geojson") as f:
                provinces_map = json.load(f)

            pyplt = py.offline.plot
            fig = px.choropleth_mapbox(
                data_frame=pd_allyear,
                geojson=provinces_map,
                color='ACCIDENT_N',
                locations="SA2_NAME16",
                featureidkey="properties.SA2_NAME16",
                mapbox_style="open-street-map",
                color_continuous_scale='YlGnBu',
                center={"lat": -37.500573, "lon": 144.583924},
                zoom=5,
                title="Accident number from 2013 to 2018",
                animation_frame="year",
            )
            pyplt(fig, filename='output\\plotly_fig4.html')
        except OSError:
            print('Please check the file path')

    def acc_age(self, pdall):
        """
        Find the proportion of elderly and young people who have accidents
        within a week
        :param pdall: the data from
        :output: save the line chart as a HTML format
        """

        pyplt = py.offline.plot
        pdall['month'] = pd.to_datetime(pdall['ACCIDENT_D'])
        pdall['month'] = pdall['month'].dt.month

        list5_12 = []
        list13_18 = []
        list_oldpe = []
        list_old_dr = []
        list_young = []

        Week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                'Saturday', 'Sunday']

        for a in Week:
            pd_a = pdall.loc[pdall.DAY_OF_WEE == a]
            pre5_12 = pd_a.loc[pd_a.PED_CYCLIS >= 1]
            pre13_18 = pd_a.loc[pd_a.PED_CYCL_1 >= 1]
            old_pe = pd_a.loc[pd_a.OLD_PEDEST >= 1]
            old_dr = pd_a.loc[pd_a.OLD_DRIVER >= 1]
            young_dr = pd_a.loc[pd_a.YOUNG_DRIV >= 1]
            list5_12.append(pre5_12['PED_CYCLIS'].sum())
            list13_18.append(pre13_18['PED_CYCL_1'].sum())
            list_oldpe.append(old_pe['OLD_PEDEST'].sum())
            list_old_dr.append(old_dr['OLD_DRIVER'].sum())
            list_young.append(young_dr['YOUNG_DRIV'].sum())

        trace1 = go.Scatter(x=Week, y=list5_12,
                            mode='lines',
                            name='PED_CYCLIST_5_12',
                            line=dict(width=4),
                            xaxis="x1",
                            yaxis="y1")
        trace2 = go.Scatter(x=Week, y=list13_18,
                            mode='lines',
                            name='PED_CYCLIST_13_18',
                            line=dict(width=4),
                            xaxis="x1",
                            yaxis="y1")
        trace3 = go.Scatter(x=Week, y=list_oldpe,
                            mode='lines',
                            name='OLD_PEDESTRIAN',
                            line=dict(width=4),
                            xaxis="x1",
                            yaxis="y1")

        trace4 = go.Scatter(x=Week, y=list_old_dr,
                            mode='lines',
                            name='OLD_DRIVER',
                            line=dict(width=4),
                            xaxis="x1",
                            yaxis="y2")
        trace5 = go.Scatter(x=Week, y=list_young,
                            mode='lines',
                            name='YOUNG_DRIVER',
                            line=dict(width=4),
                            xaxis="x1",
                            yaxis="y3")

        data = [trace1, trace2, trace3, trace4, trace5]
        layout = go.Layout(
            xaxis=dict(
                domain=[0, 0.8]
            ),
            yaxis=dict(
                domain=[0, 0.45]
            ),
            yaxis2=dict(
                domain=[0.5, 0.7]
            ),
            yaxis3=dict(
                domain=[0.75, 1]
            )
        )
        fig = go.Figure(data=data, layout=layout)
        pyplt(fig, filename='output\\plotly_fig7.html')

    def acc_type(self, pdall):
        """
       This function selects the number of UNLICENSED and ALCOHOL_related
       in a week and outputs
       :param pdall: Preprocessed data in the data preparation function
       :outputs:save the line chart as HTML format
       """

        pyplt = py.offline.plot
        Week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                'Saturday', 'Sunday']
        alc = []
        unlic = []
        for a in Week:
            pdyr = pdall.loc[pdall.DAY_OF_WEE == a]
            pd_unl = pdyr.loc[pdyr.UNLICENCSE > 0]
            pd_alc = pdyr.loc[pdyr.ALCOHOL_RE == 'Yes']
            alc.append(len(pd_alc))
            unlic.append(len(pd_unl))

        fig = go.Figure()

        fig.add_trace(go.Scatter(x=Week, y=alc,
                                 mode='lines',
                                 name='ALCOHOL',
                                 line=dict(width=4)))
        fig.add_trace(go.Scatter(x=Week, y=unlic,
                                 mode='lines',
                                 name='UNLICENCSE',
                                 line=dict(width=4)))
        pyplt(fig, filename='output\\plotly_fig6.html')

    def acc_veh(self):
        """
        This function selecting the number of different vehicle types in
        different years
        :outputs:save the line chart as HTML format
        """
        pyplt = py.offline.plot
        list_bic = []
        list_heavy = []
        list_pass = []
        list_moto = []
        list_public = []

        year = np.arange(2013, 2019)
        pd_all = pd.concat(
            [self.pd2013, self.pd2014, self.pd2015, self.pd2016, self.pd2017,
             self.pd2018], ignore_index=True)
        pd_all['month'] = pd.to_datetime(pd_all['ACCIDENT_D']).dt.month
        pd_all['year'] = pd.to_datetime(pd_all['ACCIDENT_D']).dt.year

        for a in year:
            pd_year = pd_all.loc[pd_all.year == a]
            pd_bic = pd_year.loc[pd_year.BICYCLIST >= 1]
            pd_heavy = pd_year.loc[pd_year.HEAVYVEHIC >= 1]
            pd_pass = pd_year.loc[pd_year.PASSENGERV >= 1]
            pd_moto = pd_year.loc[pd_year.MOTORCYCLE >= 1]
            pd_public = pd_year.loc[pd_year.PUBLICVEHI >= 1]

            list_bic.append(pd_bic['BICYCLIST'].sum())
            list_heavy.append(pd_heavy['HEAVYVEHIC'].sum())
            list_pass.append(pd_pass['PASSENGERV'].sum())
            list_moto.append(pd_moto['MOTORCYCLE'].sum())
            list_public.append(pd_public['PUBLICVEHI'].sum())

        trace1 = go.Scatter(x=year, y=list_bic,
                            mode='lines',
                            name='BICYCLIST',
                            line=dict(width=4),
                            xaxis="x1",
                            yaxis="y1")
        trace2 = go.Scatter(x=year, y=list_heavy,
                            mode='lines',
                            name='HEAVY',
                            line=dict(width=4),
                            xaxis="x1",
                            yaxis="y1")
        trace3 = go.Scatter(x=year, y=list_moto,
                            mode='lines',
                            name='MOTORCYCLE',
                            line=dict(width=4),
                            xaxis="x1",
                            yaxis="y1")
        trace4 = go.Scatter(x=year, y=list_public,
                            mode='lines',
                            name='PUBLIC',
                            line=dict(width=4),
                            xaxis="x1",
                            yaxis="y1")

        trace5 = go.Scatter(x=year, y=list_pass,
                            mode='lines',
                            name='PASSENGER',
                            line=dict(width=4),
                            xaxis="x1",
                            yaxis="y2")

        data = [trace1, trace2, trace3, trace4, trace5]
        layout = go.Layout(
            xaxis=dict(
                domain=[0, 0.9]
            ),
            yaxis=dict(
                domain=[0, 0.75]
            ),
            yaxis2=dict(
                domain=[0.77, 0.98]
            ),
        )

        fig = go.Figure(data=data, layout=layout)
        pyplt(fig, filename='output\\plotly_fig5.html')

    def acc_heat(self, pdall):
        """
        This function outputs a heat figure for illustrating the pattern of
        accident numbers in a year and a week
        :param pdall: Preprocessed data in the data preparation function
        :outputs:save the heat figure as HTML format
        """

        pyplt = py.offline.plot
        data = []
        pdall['month'] = pd.to_datetime(pdall['ACCIDENT_D'])
        pdall['month'] = pdall['month'].dt.month
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
                  'Sep', 'Oct', 'Nov', 'Dec']
        labels = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
        Week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                'Saturday', 'Sunday']
        for i in range(1, 13):
            length = []
            for j in Week:
                pd_week = pd.DataFrame()
                pd_week = pdall.loc[pdall['DAY_OF_WEE'] == j]
                pd_month = pd_week.loc[pd_week['month'] == i]
                length.append(len(pd_month))
            data.append(length)

        fig = go.Figure(data=go.Heatmap(
            z=data,
            x=labels,
            y=months,
            hoverongaps=False,
            colorscale='Reds'))
        pyplt(fig, filename='output\\plotly_fig8.html')
