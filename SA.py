import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
from textblob import TextBlob
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
samplecnt = 0

# Custom Variables
# Sample Size (How many reviews to read)
sample = 10000
# Printing Negative samples count
commentsample = 5

dataset = dataset.sample(sample)
print("Processing the first " + str(sample) +" Entries in the " + "Dataset...\n")
for x in range(0, len(dataset)):
    CatArray.append(dataset.iloc[x]["product_category"])
    TitleArray.append(dataset.iloc[x]["product_title"])
    CommentArray.append(dataset.iloc[x]["review_body"])
    StarArray.append(dataset.iloc[x]["star_rating"])
    ProdArray.append(dataset.iloc[x]["product_id"])

# Use textblob to get the sentiment polarity score from review_body, which is the actual written review
print("Analyzing Sentiment...\n")
for i in range(0, len(dataset)):
    t = TextBlob(dataset.iloc[i]["review_body"])
    SentScoreArray.append(t.sentiment.polarity)

print("Data Analyzed...")
print("Printing the first " + str(commentsample) + " Negative Comments\n")

for s in range(0, len(SentScoreArray)):
    if(SentScoreArray[s] == 0):
        sentTextArray.append("Neutral")
        
    if(SentScoreArray[s] > 0):
        sentTextArray.append("Positive")
        
    if(SentScoreArray[s] < 0):
        sentTextArray.append("Negative")

        if(samplecnt < commentsample):

            print("Comment Number " + str(s) + " | SENTIMENT: Negative")
            print("Comment Content : "  + CommentArray[s] + "\n")
            samplecnt = samplecnt + 1