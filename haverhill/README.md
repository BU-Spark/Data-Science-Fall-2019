# CS-506-Project
### **Team-1 project for CS 506**

### Haverhill 311 Service Request Analysis

### Summary

City of Haverhill is interested in improving and refining their decision-making process from insights born out of data analysis and visualization. The 311-system set up receives non-emergency requests such as Highway street improvements, street light repairs, etc. All relevant details regarding the issue are stored in QAlert. QAlert is a citizen request management solution that has been deployed by the City of Haverhill. The data stored in QAlert serves as a good repository to analyze and visualize. Having access to such data will help us find the underlying patterns and points of interest. The data was made available to us in a .csv format.

### Problem Statement

To assist City of Haverhill in assembling and using 311 data, complaint and information for better insights into providing more effective and efficient customer and municipal services in Haverhill. Specifically, we target the following points:

* To recognize the trends regarding 311 requests and closures of the request by type, time of the year, day of the year, day of the week, time of day.
* Mapping Geographic Information System (GIS) data.
* To observe how Haverhill is performing in managing and responding to 311 requests,
by issue, by department, by the time of year, day of week, etc.
* Based on past records compute request response time, which would be
communicated to citizens.

### **Requirements**

*sklearn 0.19.1*

*numpy 1.16.3*

*matplotlib 2.2.2*

*pandas 0.25.3*

*seaborn 0.8.1*

*folium 0.10.0*

*tqdm 4.26.0*

*geopandas 0.6.2*

*contextily 1.0rc2*

*descartes 1.1.0*

### **How to run**

Since our code is just a notebook you run individual cells or just perform run all
Note: the path of the data being read in the notebooks should be as follows:
* haverhill_analysis.ipynb
  - ./haverhill-request/haverhill-activity.csv
  - ./haverhill-request/haverhill-request.csv
* geodata.ipynb
  - ./Hav_Precincts&Wards_Shp/Precincts_Wards.shp

### **References**

* http://geopandas.org
* https://automating-gis-processes.github.io/CSC/course-info/course-info.html
* https://www.spatialreference.org/ref/epsg/2249/
* https://towardsdatascience.com/easy-steps-to-plot-geographic-data-on-a-map-python-11217859a2db
* https://www.openstreetmap.org/export#map=13/42.7829/-71.0817
