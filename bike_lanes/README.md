# CS506_Bike_Lane Team
Team Member: Mingdao Che, Yuncheng Zhu, Zhengyang Tang <br>
To Analyze the data of Boston Bike to figure out the correlation between bike crashes, bike count, businesses and bike lane blocks.<br>


## Deployment Instructions

These instructions will help you to run this project on your own machines or platforms.

### Prerequisites

#### Package:
Python Version: 3.6/3.7 - https://www.python.org/downloads/<br>		

Type command: `pip3/pip install -r requirements.txt` in the terminal of outside folder (which has requirements.txt) to install all the packages.

#### Software:

Normal IDE for python like pycharm will work.

Jupiter/Jupiter Lab is needed for some of our code (.ipynb files).

#### Dataset:
Following dataset are the dataset we used in our code, you need download all these data in the src folder to run our code succesfully.

- 311 Service Requests: https://data.boston.gov/dataset/311-service-requests

- Bike Count Data: https://www.boston.gov/departments/boston-bikes/bike-data

- Cambridge 311 Data: https://data.cambridgema.gov/browse?q=bike

- Bike Crash Data: https://data.boston.gov/dataset/vision-zero-crash-records

- HSIP Bicycle Crash Clusters 2007 - 2016: https://geo-massdot.opendata.arcgis.com/datasets/hsip-bicycle-crash-clusters-2007-2016

#### Key needed: 
Google Maps Places API Key: https://developers.google.com/places/web-service/get-api-key<br>

## Running the source code

1. Run 'bike_lane_filter.ipynb' to create the bike_block.csv file, which is the filtered bike block data.

2. Run 'problem_3.py' to create the processed bike block data (Boston_Cambridge.csv) of both Boston and Cambridge's 311 data.

3. Run the other code named by the problem's name or problem's number.

Note:

- The code files end with .ipynb are the Jupiter version and need to use Jupiter/Jupiter Lab to run the program.

- Put your key into 5th and 9th cell in correlation_block_businesses.ipynb to use google map API to find the nearby businesses.

## Result:
The conclusion and the visualizations we got for each problem is shown in the report pdf.
## Authors

* **Mingdao Che** - *nan* - [Repo](https://github.com/mdche001/)
* **Yuncheng Zhu** - *nan* [Repo](https://github.com/YanzuWuu)
* **Zhengyang Tang** - *nan*[Repo](https://github.com/ZhengyangTang)
