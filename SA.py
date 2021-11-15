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

# Read the generated dataset file
print("Importing converted Dataset file...\n")
dataset = pd.read_csv("dataset.csv",low_memory=False,error_bad_lines=False,warn_bad_lines=False)

# Static Variables
CatArray = []
TitleArray = []
CommentArray = []
StarArray = []
ProdArray = []
SentScoreArray = []
sentTextArray = []

for x in range(0, len(dataset)):
    CatArray.append(dataset.iloc[x]["product_category"])
    TitleArray.append(dataset.iloc[x]["product_title"])
    CommentArray.append(dataset.iloc[x]["review_body"])
    StarArray.append(dataset.iloc[x]["star_rating"])
    ProdArray.append(dataset.iloc[x]["product_id"])

