from csv import reader
import csv
import pdb
# skip first line i.e. read header first and then iterate over each row od csv as a list
with open('./data/data_esc_test.csv', 'w') as csv_file:
    #csv_reader = reader(read_obj)
    csv.writer(open(''))
    csvwriter = csv.writer(csvfile)
    # Check file as empty
    if header != None:
        # Iterate over each row after the header in the csv
        for row in csv_reader:
            #pdb.set_trace()
            row.append(1000000)
            # row variable is a list that represents a row in csv
            print(row)