import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
from textblob import TextBlob
import wget
import os
# Disable TF warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import requests
import webbrowser

# Flair
from flair.models import TextClassifier
from flair.data import Sentence


# Load english sentiment
classifier = TextClassifier.load('en-sentiment')

# Variables
yes = ['y' , 'Y']
no = ['n' , 'N']
CatArray = []
TitleArray = []
CommentArray = []
StarArray = []
ProdArray = []
TitleArrayInfo = []
ProdArrayInfo = []
SentScoreArray = []
sentTextArray = []
cntpos = 0
cntneg = 0
cntnet = 0
legacy = 0
commentsample = 0

# Disable file size check when debugging
debug=1

# Amazon AWS Dataset Array

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


############# Dataset Downloader
print("\033[1;33;40mGathering Data from AmazonAWS, Please wait...")

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

# Dataset file name / path
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

############# Dataset Preperations

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
dataset = pd.read_csv("dataset.csv",low_memory=False,error_bad_lines=False,warn_bad_lines=False,encoding='utf8')
dfinfo = pd.read_csv("dataset.csv",low_memory=False,error_bad_lines=False,warn_bad_lines=False,encoding='utf8')
dataset.sort_values(by=['product_title'])
dfinfo.sort_values(by=['product_title'])

############# Custom user Variables
# Sample size variable
while True:
    sample = input("\033[1;33;40mThere are \033[1;32;40m" + str(len(dataset)) + "\033[1;33;40m Samples found | " + "Enter the number of samples you want analyzed...\n\033[1;37;40m")
    if sample.isnumeric():
        sample = int(sample)
        dataset = dataset.sample(sample)
        dfinfo = dfinfo.sample(sample)
        if sample > len(dataset):
            print("\033[1;31;40mYour Requested sample size of \033[1;37;40m" + str(sample) + "\033[1;31;40m is greater than the length of your dataset!")
            print("\033[1;31;40mSample size is adjusted to max dataset size of \033[1;37;40m" + str(len(dataset)))
            sample = len(dataset)
            dataset = dataset.sample(sample)
            dfinfo = dfinfo.sample(sample)
        break
    else:
        print("\033[1;31;40mPlease Enter a positive number!\033[1;37;40m")


while True:
    classify = input("\033[1;33;40mType Yes to scan a specific product, otherwise scan the entire category (y,n)\n\033[1;37;40m")
    if classify in no:
        classify="0"
        break
    elif classify in yes:
        classify="1"
        break
    else:
        print("\033[1;31;40mEnter either Y or N\033[1;37;40m")

# Algo
while True:
    legacy = input("\033[1;33;40mType 1 to use TextBlob (Nayive Bayes) or 2 to use Flair (Custom Algo) \n\033[1;37;40m")
    if legacy.isnumeric() and legacy == "1":
        legacy = "1"
        print("\033[1;31;40mUsing TextBlob...\033[1;37;40m")
        break
    elif legacy.isnumeric() and legacy == "2":
        legacy = "0"
        print("\033[1;31;40mUsing Flair...\033[1;37;40m")
        break
    else:
        print("\033[1;31;40mPlease Enter one or two\033[1;37;40m")

if (classify == "1"):
############# Product_ID Display
    dfinfo.drop_duplicates(subset ="product_id",
                     keep = "first", inplace = True)

    if os.path.exists("product_info.txt"):
        os.remove("product_info.txt")

    txt = open("product_info.txt", "w", encoding="utf-8")
    for x in range(0, len(dfinfo)):
        TitleArrayInfo.append(dfinfo.iloc[x]["product_title"])
        ProdArrayInfo.append(dfinfo.iloc[x]["product_id"])
        txt.write("Product Name: " + TitleArrayInfo[x] + "\nSearchable ID: " + ProdArrayInfo[x])
        txt.write("\n#########################\n")
    txt.close()

    while True:
        prodprint = input("\033[1;33;40mType yes to open the Avalible products in your texteditor, otherwise print in the command-line (y,n)\n\033[1;37;40m")
        if prodprint in no:
            for x in range(0, len(dfinfo)):
                print(str(x+1)  + " Product " + dfinfo.iloc[x]["product_title"] + " Searchable ID : " +  dfinfo.iloc[x]["product_id"] + "\n")
            break
        elif prodprint in yes:
            webbrowser.open("product_info.txt")
            break
        else:
            print("\033[1;31;40mEnter either Y or N\033[1;37;40m")

    while True:
        spec_prod = input("\033[1;31;40mPlease copy the desired product ID from your text editor, and paste it here\n\033[1;37;40m")
        if not spec_prod:
            print("\033[1;31;40mPlease enter a product ID\n\033[1;37;40m")
        else:
            break
    print("\033[1;33;40mWe will scan " + str(spec_prod) + "\n\033[1;37;40m")
    dataset = dataset[dataset['product_id'] == spec_prod]

# Polarity display count
while True:
    commentsample = input("\033[1;33;40mHow many comments do you want displayed for each polarity?\n\033[1;37;40m")
    if commentsample.isnumeric():
        commentsample = int(commentsample)
        break
    else:
        print("\033[1;31;40mPlease Enter a positive number!\033[1;37;40m")

# Display negative comments
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

# Display Neutral comments
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

# Display Positive comments
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

    # Display Positive comments
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

############# Dataset manipulation / textblob

# Create arrays out of dataset
print("\033[1;32;40mProcessing " + str(sample) +" Entries in the " + "Dataset...\n")
for x in range(0, len(dataset)):
    print(f"{x/len(dataset)*100:0.1f} %", end="\r")
    CatArray.append(dataset.iloc[x]["product_category"])
    TitleArray.append(dataset.iloc[x]["product_title"])
    CommentArray.append(dataset.iloc[x]["review_body"])
    StarArray.append(dataset.iloc[x]["star_rating"])
    ProdArray.append(dataset.iloc[x]["product_id"])

# Use textblob to get the sentiment polarity score from review_body, which is the actual written review
print("\033[1;32;40mAnalyzing Sentiment...\n")
if legacy == "1":
    for i in range(0, len(dataset)):
            t = TextBlob(dataset.iloc[i]["review_body"])
            print(f"{i/len(dataset)*100:0.1f} %", end="\r")
            SentScoreArray.append(t.sentiment.polarity)
else:
    for s in range(0, len(dataset)):
            sentence = Sentence(dataset.iloc[s]["review_body"])
            classifier.predict(sentence)
            SentScoreArray.append(sentence.labels)
            score = sentence.labels
            print(f"{s/len(dataset)*100:0.1f} %", end="\r")
            if "POSITIVE" in str(score):
                sentTextArray.append("Positive")
                if(cntpos < commentsample and printpos == 1):
                    if classify == "1":
                        print("\033[1;36;40mProduct Name : \033[1;33;40m" + TitleArray[s] + "\033[1;36;40m | Sentiment/Accuracy:\033[1;32;40m " + str(score) + "\n")
                        print("\033[1;36;40mComment Content : \033[1;37;40m"  + CommentArray[s] + "\n")
                    else:
                        print("\033[1;36;40mProduct Name : \033[1;33;40m" + TitleArray[s] + "\033[1;36;40m | Sentiment/Accuracy:\033[1;32;40m " + str(score) + " \033[1;36;40mProduct ID : \033[1;33;40m" + ProdArray[s] + "\n")
                        print("\033[1;36;40mComment Content : \033[1;37;40m"  + CommentArray[s] + "\n")
                cntpos = cntpos + 1  
                    
            elif "NEGATIVE" in str(score):
                sentTextArray.append("Negative")
                if(cntneg < commentsample and printneg == 1):
                    if classify == "1":
                        print("\033[1;36;40mProduct Name : \033[1;33;40m" + TitleArray[s] + "\033[1;36;40m" + "\033[1;36;40m | Sentiment/Accuracy:\033[1;31;40m " + str(score) + "\n")
                        print("\033[1;36;40mComment Content : \033[1;37;40m"  + CommentArray[s] + "\n")
                    else:
                        print("\033[1;36;40mProduct Name : \033[1;33;40m" + TitleArray[s] + "\033[1;36;40m " + "\033[1;36;40m | Sentiment/Accuracy:\033[1;31;40m " + str(score) + " \033[1;36;40mProduct ID : \033[1;33;40m" + ProdArray[s] + "\n")
                        print("\033[1;36;40mComment Content : \033[1;37;40m"  + CommentArray[s] + "\n")
                cntneg = cntneg + 1
            else:
                sentTextArray.append("Neutral")
                if(cntnet < commentsample and printnet == 1):
                    if classify == "1":
                        print("\033[1;36;40mProduct Name : \033[1;33;40m" + TitleArray[s]  + "\033[1;36;40m | Sentiment/Accuracy:\033[1;34;40m " + str(score) + "\n")
                        print("\033[1;36;40mComment Content : \033[1;37;40m"  + CommentArray[s] + "\n")
                    else:
                        print("\033[1;36;40mProduct Name : \033[1;33;40m" + TitleArray[s] +  "\033[1;36;40m | Sentiment/Accuracy:\033[1;34;40m " + str(score) + " \033[1;36;40mProduct ID : \033[1;33;40m" + ProdArray[s] + "\n")
                        print("\033[1;36;40mComment Content : \033[1;37;40m"  + CommentArray[s] + "\n")
                cntnet = cntnet + 1
# Polarity user selection
if legacy == "1":
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
    
# Print out data to console and append them to arrays
if legacy == "1":
    for s in range(0, len(SentScoreArray)):
        if(SentScoreArray[s] == 0):
            sentTextArray.append("Neutral")
            if(cntnet < commentsample and printnet == 1):
                if classify == "1":
                    print("\033[1;36;40mProduct Name : \033[1;33;40m" + TitleArray[s] + "\033[1;36;40m | Comment Number : \033[1;33;40m" + str(s) + "\033[1;36;40m | Sentiment Accuracy:\033[1;34;40m Neutral \n")
                else:
                    print("\033[1;36;40mProduct Name : \033[1;33;40m" + TitleArray[s] + "\033[1;36;40m | Comment Number : \033[1;33;40m" + str(s) + "\033[1;36;40m | Sentiment Accuracy:\033[1;34;40m Neutral \033[1;36;40mProduct ID : \033[1;33;40m" + ProdArray[s] + "\n")
                print("\033[1;36;40mComment Content : \033[1;37;40m"  + CommentArray[s] + "\n")
                cntnet = cntnet + 1
        
        if(SentScoreArray[s] > 0):
            sentTextArray.append("Positive")
            if(cntpos < commentsample and printpos == 1):
                if classify == "1":
                    print("\033[1;36;40mProduct Name : \033[1;33;40m" + TitleArray[s] + "\033[1;36;40m | Comment Number : \033[1;33;40m" + str(s) + "\033[1;36;40m | Sentiment Accuracy:\033[1;32;40m " + str("{:.2f}".format((SentScoreArray[s] * 100))) + "% Positive \n")
                else:
                    print("\033[1;36;40mProduct Name : \033[1;33;40m" + TitleArray[s] + "\033[1;36;40m | Comment Number : \033[1;33;40m" + str(s) + "\033[1;36;40m | Sentiment Accuracy:\033[1;32;40m " + str("{:.2f}".format((SentScoreArray[s] * 100))) + "% Positive \033[1;36;40mProduct ID : \033[1;33;40m" + ProdArray[s] + "\n")
                print("\033[1;36;40mComment Content : \033[1;37;40m"  + CommentArray[s] + "\n")
                cntpos = cntpos + 1
        
        if(SentScoreArray[s] < 0):
            sentTextArray.append("Negative")
            if(cntneg < commentsample and printneg == 1):
                if classify == "1":
                    print("\033[1;36;40mProduct Name : \033[1;33;40m" + TitleArray[s] + "\033[1;36;40m | Comment Number : \033[1;33;40m" + str(s) + "\033[1;36;40m | Sentiment Accuracy:\033[1;31;40m " + str("{:.2f}".format((SentScoreArray[s] * -100))) + "%  Negative \n")
                else:
                    print("\033[1;36;40mProduct Name : \033[1;33;40m" + TitleArray[s] + "\033[1;36;40m | Comment Number : \033[1;33;40m" + str(s) + "\033[1;36;40m | Sentiment Accuracy:\033[1;31;40m " + str("{:.2f}".format((SentScoreArray[s] * -100))) + "%  Negative \033[1;36;40mProduct ID : \033[1;33;40m" + ProdArray[s] + "\n")
                print("\033[1;36;40mComment Content : \033[1;37;40m"  + CommentArray[s] + "\n")
                cntneg = cntneg + 1


# To Do: Implement Star rating
# To Do : export csv 

# Output a new CSV file with used information + sentiment values
#outframe = pd.DataFrame({'product_category':CatArray,'product_parent':ProdArray, 'product_title':TitleArray, 'Review':CommentArray, 'Star Rating':StarArray, 'Sentiment Score':SentScoreArray, 'Sentiment Polarity':sentTextArray})
#tmp = sum(SentScoreArray) / len(SentScoreArray)
#if classify == "1":
#    print("Average Sentiment of Product " + str("{:.2f}".format((tmp * 100))))
#else:
#    print("Average Sentiment of Category " + str("{:.2f}".format((tmp * 100))))
#outframe.to_csv('sentiment_on_amazon.csv')
#print(SentScoreArray.mean())
#print("\033[1;36;40mDate Exported to sentiment_on_amazon.csv")
