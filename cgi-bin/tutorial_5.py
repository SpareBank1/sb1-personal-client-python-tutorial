#!/usr/bin/env python3.7

import uuid
import cgi
import requests, json
import shelve

token_shelve = shelve.open('tokens')
access_token = token_shelve.get('access_token')

form = cgi.FieldStorage()
authorization_code = form.getvalue('code')

client_id = '<< client_id >>'
client_secret = '<< client_secret >>'
fid = '<< fid >>'

redirect_uri = "http://localhost:8000/cgi-bin/tutorial_5.py"

authorize_uri = "https://api-auth.sparebank1.no/oauth/authorize"
token_uri = "https://api-auth.sparebank1.no/oauth/token"

if ( authorization_code and not access_token ):
    data = {'grant_type': 'authorization_code', 'code': authorization_code, 'redirect_uri': redirect_uri}
    token_response = requests.post(token_uri, data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret))
    access_tokens = json.loads(token_response.content)
    access_token = access_tokens['access_token']
    token_shelve['access_token'] = access_token
    token_shelve.close()

if ( access_token ):
    api_call_headers = {'Authorization': 'Bearer ' + access_token}
    api_call_response = requests.get('https://api.sparebank1.no/personal/banking/accounts/default', headers=api_call_headers, verify=False)

    if( api_call_response.text == 'Unauthorized'):
        access_token = ''
    else: 
        response = json.loads(api_call_response.text)
        content = 'Account owner: ' + response['owner']['name']

if ( not access_token ):
    content = '<a href=' +  authorize_uri + \
        '?response_type=code&client_id=' + client_id + \
        '&redirect_uri=' + redirect_uri + \
        '&finInst=' + fid + \
        '&state=' + str(uuid.uuid4()) + \
        '>Login</a>'

print("Content-type:text/html;charset=utf-8\r\n\r\n")
print("<html>")
print("<head><title>Personal client</title></head>")
print("<body>")
print(content)
print("</body>")
print("</html>")
