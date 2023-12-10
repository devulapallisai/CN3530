import pandas as pd
import csv

df = pd.read_excel("Processed data modified.xlsx", sheet_name = "Processed data modified")

result = {}

for _, row in df.iterrows():
    sno = row['sno']
    as_number = row['as_number']
    ip_range = row['ip_range']
    geolocation = row['geolocation']
    as_name = row['as_name']
    latency = row['latency']

    key = (as_number, ip_range, geolocation, as_name)

    if key in result:
        result[key]['sno'].append(sno)
        result[key]['degree'] += 1
        result[key]['latency_sum'] += latency

    else:
        result[key] = {
            'sno': [sno],
            'degree': 1,
            'latency_sum': latency
        }

for key in result:
    result[key]['average_latency'] = result[key]['latency_sum'] / result[key]['degree']

with open("Nodes.csv", 'w', newline = '') as csvfile:
    writer = csv.writer(csvfile)

    fieldnames=["as_number", "ip_range", "geolocation", "as_name", "sno", "degree", "latency_sum", "average_latency"]

    writer.writerow(fieldnames)

    for item in result.items():
        row = [item[0][0], item[0][1], item[0][2], item[0][3], item[1]['sno'], item[1]['degree'], item[1]['latency_sum'], item[1]['average_latency']]
        writer.writerow(row)