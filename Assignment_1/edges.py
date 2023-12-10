import pandas as pd
import csv

df = pd.read_excel("Nodes modified.xlsx", sheet_name = "Nodes modified")

result = {}

for index, row in df.iterrows():
    ip_range = row['ip_range']
    node = row['node']

    key = (ip_range)
    result[key] = {
        'node': node
    }

df = pd.read_excel("Processed data modified.xlsx", sheet_name = 'Processed data modified')

items = []

for index, row in df.iterrows():
    sno = row['sno']
    as_number = row['as_number']
    ip_range = row['ip_range']
    node = result[ip_range]
    items.append([sno, as_number, ip_range, node['node']])

with open("Intermediate edges.csv", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    fieldnames = ["sno", "as_number", "ip_range", "node"]

    writer.writerow(fieldnames)

    for item in items:
        row = [item[0], item[1], item[2], item[3]]
        writer.writerow(row)

read_file = pd.read_csv("Intermediate edges.csv")
read_file.to_excel("Intermediate edges.xlsx", index = None, header=True, sheet_name='Intermediate edges')

excel_file = "Intermediate edges.xlsx"

sheet_name = 'Intermediate edges'

df = pd.read_excel(excel_file, sheet_name=sheet_name)

result = {}
items = []

for i in range(0, len(df) - 2):
    row1 = df.iloc[i]
    row2 = df.iloc[i + 1]

    node1 = row1['node']
    sno1 = row1['sno']
    node2 = row2['node']
    sno2 = row2['sno']

    if sno1 != sno2:
        continue
    if node1 == node2:
        continue

    items.append([node1,node2])

with open("Edges.csv", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    fieldnames=["node1","node2"]

    writer.writerow(fieldnames)

    for item in items:
        row = [item[0], item[1]]
        writer.writerow(row)