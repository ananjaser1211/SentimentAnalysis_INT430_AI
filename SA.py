import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import os

# Data set File name / path
dataset_file='amazon_reviews_us_Mobile_Electronics_v1_00.tsv'

# Convert amazon dataset to CSV container
# Delete previously generated dataset files
old_dataset = 'dataset.csv'
if os.path.exists(old_dataset):
    print("Clean up old datasets...")
    os.remove(old_dataset)
print("Preparing Dataset file " + os.path.splitext(dataset_file)[0] + "...")
print("Converting Dataset to supported CSV format... \nIgnoring broken entries...")
csv_table=pd.read_table(dataset_file,sep='\t',error_bad_lines=False,warn_bad_lines=False)
csv_table.to_csv('dataset.csv',index=False)
