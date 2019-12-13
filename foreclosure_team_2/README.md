# City_Foreclosure_Analysis

The drastic rise in the number of foreclosed houses across the city has resulted in homes that are left empty as families are forced to move out. These homes are frequently retaken by banks and large financial and real estate institutions that have little to no connection with the municipality in which they own property making enforcement of the building and sanitary codes very difficult. Furthermore, the
homes sit empty for months or years at a time awaiting foreclosure sale; often creating an unattractive public nuisance.
Given that the City owns a number of properties, being able to figure out what factors caused a property to foreclose, will allow the city to step in and intervene.

Goals

Figure out:
- What factors cause homes to be foreclosed
- In what neighborhoods are most foreclosures taking place
- What city-owned properties are likely to be up for foreclosure


## Installation

- You can directly run code in any python friendly IDE or platform such as PyCharm.

## Data Preprocessing

- **_311_preprocess.py_** in main directory can preprocess the raw data from 311 requests and categorize the reasons into 1 and 0.

## Data Visuallization

- data visuallization is available under [project_visuallization](https://github.com/leonshen95/City_Foreclosure_Analysis/tree/master/project_visualization). In this folder, you can run **_311_processing.py_**, **_criminal_processing.py_** and **_foreclosure_processing.py_** to see the visuallization for different data sources. 

## Train and Predict

- You can train and build model under [training](https://github.com/leonshen95/City_Foreclosure_Analysis/tree/master/training) 
- **_311_feature.py_** helps to preprocess the 311 requests data and determine the potential foreclosure data. 
- **_foreclosure.ipynb_** is used to train and build the model. 
- The result would be training accuracy and a heat map distribution of property foreclosure.
