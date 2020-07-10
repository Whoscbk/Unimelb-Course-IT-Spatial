
add_dataset <br>
===========
This folder include all the additional datasets we used in this project. <br>

When using the original data set (RegionsLGA_2017), some problems occurred like LGA names are inconsistent to VicRoadsAccident.<br>
Therefore, we use QGIS to fix these problems and export the right version for complementing the Task.<br>

LGA <br>
----
Used in Task 1.3 <br>
Fix the LGA name issues and remove some point type(Since Geopandas require consistent geometry type when drawing the choropleth maps) <br>
Export by QGIS<br>

LGA_task2 <br>
---------
Used in Task 2.1 <br>
Fix the LGA name issues <br>
Export by QGIS<br>

Vic.geojson <br>
------------
Used in Task 3 <br>
Since Plotly require Geojson type to draw the choropleth maps, we transfer the RegionsSA2_2016.shp into .geojson<br>

Weather_Condition.csv <br>
---------------------
The historical daily weather data from 2013 to 2018 <br>
[Source](http://www.bom.gov.au/climate/data-services/station-data.shtml) <br>

future_weather.csv <br>
---------------------
The forecasted weather data from 16/6/2020 to 25/6/2020 <br>
Summary from [Source](http://www.bom.gov.au/climate/data-services/station-data.shtml) <br>




15/06/2020
