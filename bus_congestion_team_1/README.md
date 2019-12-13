# Preprocessing the Data

Due to the limitation of github, we are not able to upload dataset, since it is larger than 25 MB.

Run data.py, sorting dataset/metadata.csv and splitting it into files based on date, each file is one day. All files are located in dataFolder.

To decrease the number of data rows, run clean_data.py, which will merge all data in one minute into one row. This action will truncate the data to approximately 1/6 of the original dataset. At the same time, for the reason that buses cannot move a long distance in 1 minutes, we do not lose too much information.

Once data is cleaned and reduced, using api.py on the bus data directory will allow the selection of a date and will pull and create a copy dataframe file with all entries labeled with road name and speed limit. This file requires an api key from Microsoft Bing's snap to roads API and will need to be set to APIKEY at the top of the file.

Once the directory will seperate dates of labeled data is established you are able to run any of the Q1-Q3 files to gain our results from analysis.

# Question Solving

Run Q1.py, get a folder of result named Q1_results.
Run Q2.py get a result file named Q2_results.csv.
To process Q1 and Q2, open Q1_Q2_analysis.ipynb in jupyter notebook. It will print the results as the Q1_Q2_analysis.pdf does.

Run Q3.ipynb, you can get a list of .csv files in API_dataset, processing them and getting the results as the Q3_analysis.pdf does.
