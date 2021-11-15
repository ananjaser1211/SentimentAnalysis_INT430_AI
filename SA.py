import pandas as pd

# Data set File name / path
dataset_file='amazon_reviews_us_Mobile_Electronics_v1_00.tsv'

# Convert amazon dataset to CSV container
print("Preparing Dataset file ...")
print("Converting Dataset to supported CSV format... \nIgnoring broken entries...")
csv_table=pd.read_table(dataset_file,sep='\t')
csv_table.to_csv('dataset.csv',index=False)
