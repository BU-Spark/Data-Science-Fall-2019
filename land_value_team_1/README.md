# CS506-Conservation-Easement-Value-Project

## Team Member: Qingyang Xu, Kailun Li, Ziyu Shen, Chenhao Tao


## Introduction of our Methodology

Our goal in this project is to find the impact of easement on the sale price of the land. Because the limited amount of data we have for land with easement, we decided to first create a predictive model for sale price based on the data of land without easement, which contributes to over 90% of the whole dataset. Once we got the predictive model, we would use it to predict the sale price for land with easement. By comparing the difference between the two prices (predicted sale price without easement and the real sale price with easement), we would identify the impact of easement on the sale price of land. 

For predictive models, we were choosing between Linear Regression, RandomForest Regressor, Gradient Boosting Regressor, and DecisionTree Regressor. By comparing the MAE on each regression model, we decided to use RandomForest Regressor since it gave us the lower MAE. 
 
After choosing the model with the lowest MAE which is RandomForest Regressor, we train the model with the variables we chose with parameters n_estimators = 100 and max_depth = 11 (Explained in Model Evaluation). Then, we used our predictive model to predict the sale price of the properties with easement. 

Lastly, we will use the formula below to estimate the impact of easement the sale price of properties: 
Impact of Easement = {(Estimated Sale Price - Real Sale Price) / Real Sale Price}* 100%


### Packages Using
pandas, numpy, seaborn, matplotlib, math, sklearn, statistics


### Running
Open the file called "CS 506 Property Value Modeling Project Cleaned .ipynb" using Jupyter Note Book

Click "Run All" in Cell Tab in the top

It will show the final result in the last cell


