# CS506-Final-Project
Property Value Modeling Project -- Colorado Team 

Team members: Siyi Liu, Jinshu Yang, Zixin Zhang

## File Description
### Dataset
All the data set is larger than the maximum limit of upload, please contact the team members if needed with the permission of clients. <li>
pc_spark.csv: the original dataset <li>
full_train.csv: The dataset after cleaning and feature extraction.

### Colorado_source.py:
This file generates the initial visualization of the variables. Including the distribution of important variables that are used later on in the models, scatter plot that shows the relationship between important independent variables and y, correlation matrix, and scatterplot matrix.

### Colorado_preprocess.py:
The code in this file handles data cleaning process and feature engineering based on the original dataset "pc_spark.csv". The resulting dataset after cleaning and feature extraction is saved as "full_train.csv".

### Colorado_model.py:
This file contains all the methodologies we tried. Including Linear regression, Gradient Boosting, Random Forest, Adaboost and Extra Tree. K-Fold Cross validation is used to compare the performance of each model based on their Mean Absolute Error(MAE). It also includes some vairable selection process for linear regression and random forest, and other feature we tried to modify such as adding one hot encoder. The last part of code apply the model to compute the final result. The full dataset is split into two parts: land without easement as the training set, and land with easement as the testing set. We apply our best model in predicting land price (ranodm forest) to compare the land price between with and without easement. Running the code directly prints out the final results when comparing land price with and without easement using random forest model (n_estimators = 300, max_depth = 22).

### model.ipynb:
This shows the detail of the variable selection, parameter tuning process and cross validation of our final random tree model.

### matching.R:
This file is written in R that uses matching methods to get the estimated differece between land with and without easement. Final result is based on log_price_per_ha. Note: package "matching" must be installed.
