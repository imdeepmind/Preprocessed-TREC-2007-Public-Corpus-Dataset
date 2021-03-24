import os
import re
import email
import pandas as pd
from tqdm import tqdm

from utils import clean_message

# Constants
DATA_PATH = 'data/trec07p/data'
LABEL_PATH = 'data/trec07p/full/index'

# Reading the 
print("--> Reading the label file...")
labels = pd.read_csv(LABEL_PATH, sep=' ', header=None)

print("--> Preprocessing the contents of the label file...")
# Dropping any na values
labels.dropna(inplace=True)

# Adding columns to the DF
labels.columns = ['label', 'id']

# Changing to word spam and ham to 1 and 0
labels['label'] = labels['label'].apply(lambda x: 1 if x=='spam' else 0)

# For id column, storing just the id
labels['id'] = labels['id'].apply(lambda x: x.split('/')[2])

# Converting the DataFrame to numpy array
labels_array = labels.values    

print(f"--> There is {len(labels_array)} items in the label file...")

# Making a DataFrame to store the data
print("--> Creating a new DataFrame to store the preprocessed data...")
emails = pd.DataFrame(columns=["label", "subject", "email_to", "email_from", "message"])

# Iterating through all the files
for index, (label, email_id) in tqdm(enumerate(labels_array)):
    with open(os.path.join(DATA_PATH, email_id), "r", encoding='ISO-8859-1') as f:
        # Reading the file
        email_content = f.read()
        
        # Parsing the content using message_from_string func
        parsed_email_content = email.message_from_string(email_content)
        
        # Extracting the subject, email_to and email_from
        subject = parsed_email_content["subject"]
        email_to = parsed_email_content["to"]
        email_from = parsed_email_content["from"]
        
        # Extracting the body of the email
        message = ""
        
        if parsed_email_content.is_multipart():
            for payload in parsed_email_content.get_payload():
                message += str(payload)
        else:
            message = parsed_email_content.get_payload()
        
        message = clean_message(message)
        
        # Pushing the data into the DataFrame
        emails.loc[index] = [label, subject, email_to, email_from, message]

# Finally storing the data into a CSV file for futher use
print("--> Saving the data into CSV file...")
emails.to_csv("data/processed_data.csv", index=False)