import requests
import json
import os
from datetime import datetime
from tkinter import filedialog
import time
# Define the specific location where you want to create the folder
direct =  str(filedialog.askdirectory(title="Save at"))

# Get today's date and format it as a string
today = datetime.now().strftime('%Y-%m-%d')

# Combine the location with the folder name (today's date)
folder_path = os.path.join(direct, today)

os.makedirs(folder_path,exist_ok= True)
 
    
surveylist = ["SV_XXXXXXX","SV_XXXXXXX"] #Your questionnaire ID


headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-API-TOKEN": "XXXX",#your token
}
progressids = []
fileids = []
Datacenter_ID = "syd1" #Get it from account setting

#Download the files function
def download ():
        link = requests.get(
            'https://{Datacenter}.qualtrics.com/API/v3/surveys/{surveyid}/export-responses/{fileid}/file'.format(surveyid=i, Datacenter=Datacenter_ID,fileid=fileid ),
            headers=headers,
        )
        file_path = os.path.join(folder_path, '{surveyid}.zip'.format(surveyid=i))
        with open(file_path, 'wb') as f:
             f.write(link.content)
             
# for loop for running through the surveylist
for i in surveylist:

    url = "https://{Datacenter}.qualtrics.com/API/v3/surveys/{surveyid}/export-responses".format(surveyid = i, Datacenter=Datacenter_ID )
    
    data = {
        "format": "csv",
        "useLabels": True,
        "timeZone": "Asia/Hong_Kong"
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    print(response.status_code)
    print(response.text)
    response_dict = json.loads(response.text)
    progressid = response_dict['result']['progressId']
    progressids.append(progressid)
    
# Since it take time for generating CSV, The program will pause for 3 min, change it base on the no. of your respondents.
t = 60*3
time.sleep(t)

for i, x in zip (surveylist, progressids) :

    response = requests.get(
        'https://{Datacenter}.qualtrics.com/API/v3/surveys/{surveyid}/export-responses/{progressid}'.format(surveyid=i, Datacenter=Datacenter_ID, progressid = x),
        headers=headers,
    )
    response_dict = json.loads(response.text)
    fileid = response_dict['result']['fileId']
    completestatus = response_dict['result']['percentComplete']
    fileids.append(fileid)
    if completestatus == 100:
        download ()
    else:    
        #Just in case of the generation is not complete, wait extra time and run the process again. 
        t = 60*3
        download ()
