from __future__ import print_function
import requests
import json
import csv
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

auth="CWB-C216538E-45E8-4FB5-BFAD-09ACD2B62F94"
base='https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/'
dataid="O-A0001-001"
stationid='466990'
elem="TEMP"
form='JSON'
limit=15

res=requests.get(f'{base}{dataid}?Authorization={auth}&stationId={stationid}&elementName={elem}&format={form}&limit={limit}')

print(res.status_code)
d=json.loads(res.content.decode('utf-8'))

with open('weather.json','w') as f:
    json.dump(d,f)

temp=d['cwbopendata']['location'][0]['weatherElement'][3]['elementValue']
loca=d['cwbopendata']['location'][0]['locationName']
tp=json.dumps(temp,indent=4)
lo=json.dumps(loca,indent=4)
print(tp.encode('utf-8').decode('unicode_escape'))
print(lo.encode('utf-8').decode('unicode_escape'))

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))

main()
