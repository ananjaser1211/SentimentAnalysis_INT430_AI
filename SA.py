import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
from textblob import TextBlob
import wget
import tarfile
import os
import requests

# Vairables
# user input
yes = ['y' , 'Y']
no = ['n' , 'N']

datasets_url = [
'https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Watches_v1_00.tsv.gz',
'https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Video_Games_v1_00.tsv.gz',
'https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Video_v1_00.tsv.gz',
'https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Toys_v1_00.tsv.gz',
'https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Tools_v1_00.tsv.gz',
'https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Software_v1_00.tsv.gz',
'https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Shoes_v1_00.tsv.gz',
'https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Pet_Products_v1_00.tsv.gz',
'https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Personal_Care_Appliances_v1_00.tsv.gz',
'https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_PC_v1_00.tsv.gz',
'https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Outdoors_v1_00.tsv.gz',
'https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Office_Products_v1_00.tsv.gz',
'https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Musical_Instruments_v1_00.tsv.gz',
'https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Mobile_Electronics_v1_00.tsv.gz',
'https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Major_Appliances_v1_00.tsv.gz',
'https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Luggage_v1_00.tsv.gz',
'https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Jewelry_v1_00.tsv.gz',
'https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Home_Improvement_v1_00.tsv.gz',
'https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Home_Entertainment_v1_00.tsv.gz',
'https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Grocery_v1_00.tsv.gz',
'https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Gift_Card_v1_00.tsv.gz',
'https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Furniture_v1_00.tsv.gz',
'https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Electronics_v1_00.tsv.gz',
'https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Digital_Video_Games_v1_00.tsv.gz',
'https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Digital_Video_Download_v1_00.tsv.gz',
'https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Digital_Software_v1_00.tsv.gz',
'https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Digital_Music_Purchase_v1_00.tsv.gz',
'https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Digital_Ebook_Purchase_v1_01.tsv.gz',
'https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Digital_Ebook_Purchase_v1_00.tsv.gz',
'https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Camera_v1_00.tsv.gz',
'https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Beauty_v1_00.tsv.gz',
'https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Baby_v1_00.tsv.gz',
'https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Automotive_v1_00.tsv.gz',
'https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Apparel_v1_00.tsv.gz']

print("\033[1;33;40mGathering Data from AmazonAWS, Please wait...")

# Disable file size check when debugging
debug=1

for i in range(len(datasets_url)):
  dtname = os.path.basename(datasets_url[i])
  dtname = dtname.replace("amazon_reviews_us_","")
  dtname = dtname.replace("_v1_00.tsv.gz","")
  dtname = dtname.replace("_v1_01.tsv.gz","")
  dtname = dtname.replace("_v1_02.tsv.gz","")
  if debug == 0:
        response = requests.head(datasets_url[i], allow_redirects=True)
        size = response.headers.get('content-length', -1)
        print("\033[1;36;40mDataset Category \033[1;37;40m" + str(i+1) + "\033[1;36;40m = " + dtname + " \033[1;37;40m" + f"{'File Size'} : {int(size) / float(1 << 20):.2f} MB")
  else:
    print("\033[1;36;40mDataset Category \033[1;37;40m" + str(i+1) + "\033[1;36;40m = " + dtname)

while True:
    cat = input("\033[1;33;40mPlease type the number of the needed dataset category\n\033[1;37;40m")
    if cat.isnumeric() and int(cat) < int(len(datasets_url) + 1):
        cat = int(cat)
        print("\033[1;36;40mSelected : " + os.path.basename(datasets_url[cat-1]))
        break
    else:
        print("\033[1;31;40mPlease Enter a number within the range of avalible datasets\033[1;37;40m")

# Data set File name / path
dataset_url = datasets_url[cat-1]
fname = os.path.basename(dataset_url)
if os.path.exists(fname):
    while True:
        read = input("\033[1;33;40mDataset is downloaded already, would you like to redownload? (y,n)\n\033[1;37;40m")
        if read in yes:
                print("\033[1;36;40mDownloading \033[1;33;40m" + dataset_url + "\033[1;36;40m Dataset file...\n")
                os.remove(fname)
                dataset_file = wget.download(dataset_url)
                break
        elif read in no:
                dataset_file = fname
                break
        else:
            print("\033[1;31;40mEnter either (Y or N)\033[1;37;40m")
else:
    print("\033[1;36;40mDownloading \033[1;33;40m" + dataset_url + "\033[1;36;40m Dataset file...\n")
    dataset_file = wget.download(dataset_url)

if os.path.exists(dataset_file):
    print("\033[1;36;40m\nUsing " + os.path.splitext(dataset_file)[0] + " Dataset file...\n")
else:
    print("\033[1;31;40mDataset file is missing, Check URL")
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

            print("\033[1;36;40mProduct Name : \033[1;33;40m" + TitleArray[s] + "\033[1;36;40m | Comment Number : \033[1;33;40m" + str(s) + "\033[1;36;40m | SENTIMENT:\033[1;34;40m Neutral \n")
            print("\033[1;36;40mComment Content : \033[1;37;40m"  + CommentArray[s] + "\n")
            cntnet = cntnet + 1
        
    if(SentScoreArray[s] > 0):
        sentTextArray.append("Positive")

        if(cntpos < commentsample and printpos == 1):

            print("\033[1;36;40mProduct Name : \033[1;33;40m" + TitleArray[s] + "\033[1;36;40m | Comment Number : \033[1;33;40m" + str(s) + "\033[1;36;40m | SENTIMENT:\033[1;32;40m Positive \n")
            print("\033[1;36;40mComment Content : \033[1;37;40m"  + CommentArray[s] + "\n")
            cntpos = cntpos + 1
        
    if(SentScoreArray[s] < 0):
        sentTextArray.append("Negative")

        if(cntneg < commentsample and printneg == 1):

            print("\033[1;36;40mProduct Name : \033[1;33;40m" + TitleArray[s] + "\033[1;36;40m | Comment Number : \033[1;33;40m" + str(s) + "\033[1;36;40m | SENTIMENT:\033[1;31;40m Negative \n")
            print("\033[1;36;40mComment Content : \033[1;37;40m"  + CommentArray[s] + "\n")
            cntneg = cntneg + 1

# Output a new CSV file with used information + sentiment values
outframe = pd.DataFrame({'product_category':CatArray,'product_parent':ProdArray, 'product_title':TitleArray, 'Review':CommentArray, 'Star Rating':StarArray, 'Sentiment Score':SentScoreArray, 'Sentiment Polarity':sentTextArray})

outframe.to_csv('sentiment_on_amazon.csv')
print("\033[1;36;40mDate Exported to sentiment_on_amazon.csv")