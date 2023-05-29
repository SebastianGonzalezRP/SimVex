from numpy import random
import csv
import os

def random_value(distribution, attributes):            
        if distribution == "Exp":
            value = random.exponential(attributes["rate"])
        elif distribution == "Uniform":
            value = random.uniform(attributes["a"],attributes["b"])
        elif distribution == "Fixed":
            value = attributes["rate"]
        elif distribution == "Normal":
            value = random.normal(attributes["mu"],attributes["stdv"])
        return round(value)

def sort_file(data,sort_index):
        data = sorted(data, key=lambda x: x[sort_index])
        return data

def write_csv(data,serial,file_name):
        if not os.path.exists(f'files/{serial}'):
            os.makedirs(f'files/{serial}')
        with open(f'files/{serial}/{file_name}', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in data:
                writer.writerow(row)

def generate_route_object():
    pass