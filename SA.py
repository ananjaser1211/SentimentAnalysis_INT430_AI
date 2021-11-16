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
cntpos = 0
cntneg = 0
cntnet = 0
# user input
yes = ['y' , 'Y']
no = ['n' , 'N']

# Custom Variables
while True:
    sample = input("\033[1;33;40mHow many Samples do you want analyized?\n\033[1;37;40m")
    if sample.isnumeric():
        sample = int(sample)
        dataset = dataset.sample(sample)
        if sample > len(dataset):
            print("\033[1;31;40mYour Requested sample size of \033[1;37;40m" + str(sample) + "\033[1;31;40m is greater than the length of your dataset!")
            print("\033[1;31;40mSample size is adjusted to max dataset size of \033[1;37;40m" + str(len(dataset)))
            sample = len(dataset)
            dataset = dataset.sample(sample)
        break
    else:
        print("\033[1;31;40mPlease Enter a positive number!\033[1;37;40m")

# Print stacks of sentiments were commentsample is how many will be printed of each polarity
while True:
    commentsample = input("\033[1;33;40mHow many comments do you want displayed for each polarity?\n\033[1;37;40m")
    if commentsample.isnumeric():
        commentsample = int(commentsample)
        break
    else:
        print("\033[1;31;40mPlease Enter a positive number!\033[1;37;40m")

while True:
    printneg = input("\033[1;33;40mDo you want to print Negative comments ? (y,n)\n\033[1;37;40m")
    if printneg in yes:
        printneg = 1
        break
    elif printneg in no:
        printneg = 0
        break
    else:
        print("\033[1;31;40mEnter either Y or N\033[1;37;40m")

while True:
    printnet = input("\033[1;33;40mDo you want to print Neutral comments ? (y,n)\n\033[1;37;40m")
    if printnet in yes:
        printnet = 1
        break
    elif printnet in no:
        printnet = 0
        break
    else:
        print("\033[1;31;40mEnter either Y or N\033[1;37;40m")

while True:
    printpos = input("\033[1;33;40mDo you want to print Positive comments ? (y,n)\n\033[1;37;40m")
    if printpos in yes:
        printpos = 1
        break
    elif printpos in no:
        printpos = 0
        break
    else:
        print("\033[1;31;40mEnter either Y or N\033[1;37;40m")

print("\033[1;32;40mProcessing " + str(sample) +" Entries in the " + "Dataset...\n")
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
    print("\033[1;36;40mPrinting the first " + str(commentsample) + " Negative Comments")
else:
    print("\033[1;31;40mNegative printout is disabled!")
if (printnet == 1):
    print("\033[1;36;40mPrinting the first " + str(commentsample) + " Neutral Comments")
else:
    print("\033[1;31;40mNeutral printout is disabled!")
if (printpos == 1):
    print("\033[1;36;40mPrinting the first " + str(commentsample) + " Positive Comments")
else:
    print("\033[1;31;40mPositive printout is disabled!")
    


for s in range(0, len(SentScoreArray)):
    if(SentScoreArray[s] == 0):
        sentTextArray.append("Neutral")

        if(cntnet < commentsample and printnet == 1):

            print("\033[1;36;40mComment Number " + str(s) + " | SENTIMENT:\033[1;34;40m Neutral")
            print("\033[1;36;40mComment Content : \033[1;33;40m"  + CommentArray[s] + "\n")
            cntnet = cntnet + 1
        
    if(SentScoreArray[s] > 0):
        sentTextArray.append("Positive")

        if(cntpos < commentsample and printpos == 1):

            print("\033[1;36;40mComment Number " + str(s) + " | SENTIMENT:\033[1;32;40m Positive")
            print("\033[1;36;40mComment Content : \033[1;33;40m"  + CommentArray[s] + "\n")
            cntpos = cntpos + 1
        
    if(SentScoreArray[s] < 0):
        sentTextArray.append("Negative")

        if(cntneg < commentsample and printneg == 1):

            print("\033[1;36;40mComment Number " + str(s) + " | SENTIMENT:\033[1;31;40m Negative")
            print("\033[1;36;40mComment Content : \033[1;33;40m"  + CommentArray[s] + "\n")
            cntneg = cntneg + 1

# Output a new CSV file with used information + sentiment values
outframe = pd.DataFrame({'product_category':CatArray,'product_parent':ProdArray, 'product_title':TitleArray, 'Review':CommentArray, 'Star Rating':StarArray, 'Sentiment Score':SentScoreArray, 'Sentiment Polarity':sentTextArray})

outframe.to_csv('sentiment_on_amazon.csv')
print("\033[1;36;40mDate Exported to sentiment_on_amazon.csv")