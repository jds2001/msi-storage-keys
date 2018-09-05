#!/usr/bin/python

import requests
import sys
import os

request_headers = {}
request_headers['Metadata'] = 'true'

key=requests.get('http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/',
        headers=request_headers)

token=key.json()['access_token']
metadata=requests.get('http://169.254.169.254/metadata/instance?api-version=2017-12-01',
        headers=request_headers)
subscription=metadata.json()['compute']['subscriptionId']

rg=os.getenv('RESOURCE_GROUP', metadata.json()['compute']['resourceGroupName'])
sa=os.getenv('STORAGE_ACCOUNT', '')

if not sa:
    sys.stderr.write('storage account is required. Define STORAGE_ACCOUNT environment variable\n')
    sys.exit(1)

key_headers={}
key_headers['Content-Length'] = 0
key_headers['Authorization'] = 'Bearer {}'.format(token)

sa_keys=requests.post('https://management.azure.com/subscriptions/{}/resourceGroups/{}/providers/Microsoft.Storage/storageAccounts/{}/listKeys?api-version=2017-10-01'.format(subscription,
    rg, sa), headers=key_headers)

key1=sa_keys.json()['keys'][0]['value'] # we just want the fir
print key1
