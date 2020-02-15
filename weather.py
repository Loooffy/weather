import requests
import json
import os.path
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def cwb():
    auth="CWB-C216538E-45E8-4FB5-BFAD-09ACD2B62F94"
    base='https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/'
    dataid="O-A0001-001"
    stationid='466990'
    elem="TEMP,HUMD,PRES,SUN"
    form='JSON'
    limit=15

    res=requests.get(f'{base}{dataid}?Authorization={auth}&stationId={stationid}&elementName={elem}&format={form}&limit={limit}')

    print(res.status_code)
    d=json.loads(res.content.decode('utf-8'))

    '''
    with open('weather.json','w') as f:
        json.dump(d,f)
    '''
    
    ''' 
    for n,e in enumerate(l):
        if e['stationId']=='C0Z150':
            print(n,e['locationName'])
    '''

    elements=[]

    for n in range(0,6):
        elements.append(d['cwbopendata']['location'][62]['weatherElement'][n]['elementValue']['value'])
    loca=d['cwbopendata']['location'][62]['locationName']
    time=d['cwbopendata']['location'][62]['time']['obsTime']
    #print(tp.encode('utf-8').decode('unicode_escape'))
    data=[time]+[loca]+elements
    
    return data

def gsheet(data):
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by url
    spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1Cv_yNxLBJDLWXzgv6gWFd_Y60v-R_RAp3nrxqXMI4RA/edit#gid=0")
    sheet = spreadsheet.sheet1

    # Extract and print all of the values
    titles=['時間','站點','海拔','風向','風速','溫度','濕度','氣壓']
    sheet.append_row(data)

data=cwb()
gsheet(data)
