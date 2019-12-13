## Directory Structure

1. civil_cases.csv : Data of public civil cases from the 2008 to middle of 2018. Contains appeals and supreme judicial court.
    * Was obtained by analysing the HTML scrapes of previous team
1. criminal_cases.csv : Data of public criminal cases from the 2008 to middle of 2018. Contains appeals and supreme judicial court.
    * Was created by previous team
1. criminal_civil_cases.csv : Combined data of criminal_cases.csv and civil_cases.csv
1. processed_cases.csv : Data pre processed from criminal_civil_cases.csv with no text features
1. text_processed_cases.csv : Data pre processed from criminal_civil_cases.csv considering text features
1. text_matrix.npz : Tf-Idf result of pre_processing text features from criminal_civil_cases.csv
    * Meant to be used along with text_processed_cases.csv