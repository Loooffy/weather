import requests
import json
import csv

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
