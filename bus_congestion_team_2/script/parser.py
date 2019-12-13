import csv
import pandas as pd

BLOCK = 9
with open("../csv/rawSchoolData", 'r') as f:
	lines = f.readlines()

	schools = [x[:-1] for x in lines[::BLOCK]]
	headmasters = lines[1::BLOCK]
	streets = [x[:-1] for x in lines[2::BLOCK]]

	districts = [x[:-1] for x in lines[3::BLOCK]]
	gradesOffer = lines[4::BLOCK]
	hours = [x[7:-1] for x in lines[5::BLOCK]]
	types = lines[6::BLOCK]

	df = pd.DataFrame(list(zip(schools, hours, streets, districts)), 
		columns=['school name', 'school hour', 'street', 'area'])

	# print(df.head())
	df.to_csv("../csv/schools.csv")