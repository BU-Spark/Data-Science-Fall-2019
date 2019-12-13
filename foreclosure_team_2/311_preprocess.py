import csv

feature_list = [
    'Street Lights',
    'Sanitation',
    'Signs & Signals',
    'Highway Maintenance',
    'Notification',
    'Street Cleaning',
    'Code Enforcement',
    'Recycling',
    'Environmental Services',
    'Graffiti',
    'Building',
    'Employee & General Comments',
    'Enforcement & Abandoned Vehicles',
    'Housing',
    'Trees',
    'Health',
    'Weights and Measures',
    'Park Maintenance & Safety',
    'Abandoned Bicycle',
    'Administrative & General Requests',
    'Operations',
    'Traffic Management & Engineering',
    'Cemetery',
    'Office of The Parking Clerk',
    'Volunteer & Corporate Groups',
    'Bridge Maintenance',
    'Valet',
    'Alert Boston',
    'Parking Complaints',
    'Programs',
    'Current Events',
    'Catchbasin',
    'Water Issues',
    'Fire Hydrant',
    'School Transportation',
    'School Department',
    'Sidewalk Cover / Manhole',
    'Billing',
    'MBTA',
    'Pothole',
    'General Request',
    'Fire Department',
    'Survey',
    'Animal Issues',
    'Neighborhood Services Issues',
    'Generic Noise Disturbance',
    'Massport',
    'Noise Disturbance',
    'Air Pollution Control',
    'Administration',
    'Administrative',
    'Disability',
    'Metrolist',
    'Call Inquiry',
    'Consumer Affairs Issues',
    'Call Center Intake',
    'Investigations and Enforcement',
    'Boston Bikes',
    'Participatory Budgeting Idea Collection']

feature_idx = {}
idx = 0

for reason in feature_list:
    feature_idx[reason] = i
    idx += 1

feature_len = len(feature_list)
feature_set = set(feature_list)

with open('311.csv', 'r') as csvinput:
    with open('311_featured.csv', 'w') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        reader = csv.reader(csvinput)

        row = next(reader)
        row += feature_list
        row.append("Potential Foreclosure")
        writer.writerow(row)
        foreclosure_request = nonforeclosure_request = 0

        for row in reader:

            if "2019-10" in row[1] or "2019-11" in row[1]:
                continue

            for i in range(feature_len):
                if row[9] in feature_set and i == feature_idx[row[9]]:
                    row.append(1)
                else:
                    row.append(0)

            if row[5] == "Open" or "VIOISS" in row[6] or "VIOLFND" in row[6]:
                row.append(1)
                foreclosure_request += 1
            else:
                row.append(0)
                nonforeclosure_request += 1

            writer.writerow(row)

print(foreclosure_request)
print(nonforeclosure_request)
