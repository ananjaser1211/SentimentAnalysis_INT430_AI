import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
from textblob import TextBlob
import os

# Data set File name / path
dataset_file='amazon_reviews_us_Mobile_Electronics_v1_00.tsv'
if os.path.exists(dataset_file):
    print("\033[1;36;40mUsing " + os.path.splitext(dataset_file)[0] + " Dataset file...")
else:
    print("\033[1;31;40mDataset file is missing")
    exit()

# Convert amazon dataset to CSV container
# Delete previously generated dataset files
old_dataset = 'dataset.csv'
if os.path.exists(old_dataset):
    print("Clean up old datasets...")
    os.remove(old_dataset)
print("\033[1;36;40mPreparing Dataset file ...")
print("\033[1;36;40mConverting Dataset to supported CSV format... \nIgnoring broken entries...")
csv_table=pd.read_table(dataset_file,sep='\t',error_bad_lines=False,warn_bad_lines=False)
csv_table.to_csv('dataset.csv',index=False)

# Read the generated dataset file
print("\033[1;36;40mImporting converted Dataset file...\n")
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
sample = 100
# Printing Negative samples count
commentsample = 5
printneg = 1
printpos = 1
printnet = 1

dataset = dataset.sample(sample)

print("\033[1;32;40mProcessing the first " + str(sample) +" Entries in the " + "Dataset...\n")
for x in range(0, len(dataset)):
    print(f"{x/len(dataset)*100:0.1f} %", end="\r")
    CatArray.append(dataset.iloc[x]["product_category"])
    TitleArray.append(dataset.iloc[x]["product_title"])
    CommentArray.append(dataset.iloc[x]["review_body"])
    StarArray.append(dataset.iloc[x]["star_rating"])
    ProdArray.append(dataset.iloc[x]["product_parent"])

# Use textblob to get the sentiment polarity score from review_body, which is the actual written review
print("\033[1;32;40mAnalyzing Sentiment...\n")
for i in range(0, len(dataset)):
    t = TextBlob(dataset.iloc[i]["review_body"])
    print(f"{i/len(dataset)*100:0.1f} %", end="\r")
    SentScoreArray.append(t.sentiment.polarity)

print("Data Analyzed...")
if (printneg == 1):
    print("\033[1;36;40mPrinting the first " + str(commentsample) + " Negative Comments\n")
else:
    print("\033[1;31;40mNegative printout is disabled!")
if (printnet == 1):
    print("\033[1;36;40mPrinting the first " + str(commentsample) + " Neutral Comments\n")
else:
    print("\033[1;31;40mNeutral printout is disabled!")
if (printpos == 1):
    print("\033[1;36;40mPrinting the first " + str(commentsample) + " Positive Comments\n")
else:
    print("\033[1;31;40mPositive printout is disabled!")
    


for s in range(0, len(SentScoreArray)):
    if(SentScoreArray[s] == 0):
        sentTextArray.append("Neutral")

        if(samplecnt < commentsample and printnet == 1):

            print("\033[1;36;40mComment Number " + str(s) + " | SENTIMENT:\033[1;34;40m Neutral")
            print("\033[1;36;40mComment Content : \033[1;33;40m"  + CommentArray[s] + "\n")
            samplecnt = samplecnt + 1
        
    if(SentScoreArray[s] > 0):
        sentTextArray.append("Positive")

        if(samplecnt < commentsample and printpos == 1):

            print("\033[1;36;40mComment Number " + str(s) + " | SENTIMENT:\033[1;32;40m Positive")
            print("\033[1;36;40mComment Content : \033[1;33;40m"  + CommentArray[s] + "\n")
            samplecnt = samplecnt + 1
        
    if(SentScoreArray[s] < 0):
        sentTextArray.append("Negative")

        if(samplecnt < commentsample and printneg == 1):

            print("\033[1;36;40mComment Number " + str(s) + " | SENTIMENT:\033[1;31;40m Negative")
            print("\033[1;36;40mComment Content : \033[1;33;40m"  + CommentArray[s] + "\n")
            samplecnt = samplecnt + 1

# Output a new CSV file with used information + sentiment values
outframe = pd.DataFrame({'product_category':CatArray,'product_parent':ProdArray, 'product_title':TitleArray, 'Review':CommentArray, 'Star Rating':StarArray, 'Sentiment Score':SentScoreArray, 'Sentiment Polarity':sentTextArray})

outframe.to_csv('sentiment_on_amazon.csv')
print("\033[1;36;40mDate Exported to sentiment_on_amazon.csv")