# Start using SpareBank 1 Personal Client with Python

This tutorial gets you up and running with a simple Python based client for the SpareBank 1 Open APIs for personal clients. The script is just a demonstration, or a foundation for you to use. It assumes everything goes as planned, no error handling or testing is included

The SpareBank 1 Open APIs for personal clients use oAuth Authorization Code Flow to authenticate (RFC 6749, 4.1), and the authorization code is provided after a bankID authentication. The authorization code is then exchanged for an oAuth token, that can be used to access the APIs

The script has been created based on the documentation here: https://developer.sparebank1.no/#/documentation/gettingstarted

We are creating a script that works with production data, meaning your actual bank accounts. We do not use any APIs that modifies your accounts or transfer any money in this tutorial, we only retrieve information. For more information visit https://developer.sparebank1.no

Each step can be found as a separate python file under `cgi-bin`

Have fun!

We assume that you have an up to date Python environment running

## Set up a webserver
We need a local web server that is allowed to run python scripts. An easy solution is to use the CGIHTTPServer module.

We create a new project folder "OpenAPIPythonTutorial" and in this folder we create a script folder "cgi-bin" this is the default script folder name for the CGIHTTPServer module

Create a file in the "cgi-bin" folder: "tutorial.py"

```python
#!/usr/bin/env python3.7

content = 'Hello world'

print("Content-type:text/html;charset=utf-8\r\n\r\n")
print("<html>")
print("<head><title>Personal client</title></head>")
print("<body>")
print(content)
print("</body>")
print("</html>")
```

Save the file and make it executable

    `chmod +x cgi-bin/tutorial.py`

Start the webserver
    `python -m CGIHTTPServer`
Depending on your python version and config you might need to use `python3` instead of `python`
You might also need to use `python -m http.server --cgi` instead of `python -m CGIHTTPServer`

The webserver use port 8000 by default, you can now point your browser to [http://localhost:8000/cgi-bin/tutorial.py](http://localhost:8000/cgi-bin/tutorial.py)

## Register your application

Now you need to [log in](https://developer.sparebank1.no/#/login) to the developer portal to register your application for access

The name of the application is not important, I just called it "Python tutorial". The redirect URL must be the URL to your script. If you followed my instructions so far, it should be http://localhost:8000/cgi-bin/tutorial.py

Note down `client_id`, `client_secret` and `fid`

## Create a authorization link 

Modify "tutorial.py", as follows, and replace `<< client_id >>` and `<< client_secret >>` with the data you got from registration of your app. You may also add financial institution (`<< fid >>`), this is optional, but it improves the authorization step later

This script creates the authorization link, used to take you to the login system of SpareBank 1 and return the authorization code

```python
#!/usr/bin/env python3.7

import uuid

client_id = '<< client_id >>'
client_secret = '<< client_secret >>'
fid = '<< fid >>'

redirect_uri = "http://localhost:8000/cgi-bin/tutorial.py"
authorize_uri = "https://api-auth.sparebank1.no/oauth/authorize"

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
```

You can now go to http://localhost:8000/cgi-bin/tutorial.py again and refresh, the link should take you to the bank selector and login procedure. The script is not yet set up to handle the next step after login, so, no need to go through the process

## Handle redirect with authentication code

When you later go through with the login, you will get an authentication code back to your script. The redirect URL is used to reach your script, and a http get parameter named "code" is added, we need to modify the script to handle that


```python
#!/usr/bin/env python3.7

import uuid
import cgi

form = cgi.FieldStorage()
authorization_code = form.getvalue('code')

client_id = '<< client_id >>'
client_secret = '<< client_secret >>'
fid = '<< fid >>'

redirect_uri = "http://localhost:8000/cgi-bin/tutorial.py"
authorize_uri = "https://api-auth.sparebank1.no/oauth/authorize"

if (authorization_code):
    content = "Got the code: " + authorization_code
else:
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
```

You can now go to http://localhost:8000/cgi-bin/tutorial.py again and complete the login procedure. The script should now output the authentication code. This code is only valid for a short time, and can only be used to acquire an oAuth token

## Exchange the authentication code for an oAuth Token

Now that we have the functionality to get the authentication code, we will modify the script to exchange it for an oAuth token. We do that by introducing the "token_uri" in the script. We call this, and get a json document back, that contains the oAuth token


```python
#!/usr/bin/env python3.7

import uuid
import cgi
import requests, json

form = cgi.FieldStorage()
authorization_code = form.getvalue('code')

client_id = '<< client_id >>'
client_secret = '<< client_secret >>'
fid = '<< fid >>'

redirect_uri = "http://localhost:8000/cgi-bin/tutorial.py"

authorize_uri = "https://api-auth.sparebank1.no/oauth/authorize"
token_uri = "https://api-auth.sparebank1.no/oauth/token"

if (authorization_code):
    data = {'grant_type': 'authorization_code', 'code': authorization_code, 'redirect_uri': redirect_uri}
    token_response = requests.post(token_uri, data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret))
    access_tokens = json.loads(token_response.text)
    access_token = access_tokens['access_token']
    
    content = 'Access token: ' + access_token

else:
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
```


---
**IMPORTANT**

At this point it is prudent to remind you that the oAuth token is your personal, long lived, key to your bank accounts. It can be used to access your account information, and to transfer money from your account. Keep it safe! If you fear it may have been compromised; immediately go to the registration link for your bank (provided above) and delete the application access

---

## Save the token

We have successfully managed to get a token. The access-token token is valid for 10 minutes. In this example we choose to use python shelve to store the token for simplicity. You might want to save it to your operating system keychain or similar. Now, let's modify the script to save the token, and reuse the token if possible

```python
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

redirect_uri = "http://localhost:8000/cgi-bin/tutorial.py"

authorize_uri = "https://api-auth.sparebank1.no/oauth/authorize"
token_uri = "https://api-auth.sparebank1.no/oauth/token"

if ( authorization_code ):
    data = {'grant_type': 'authorization_code', 'code': authorization_code, 'redirect_uri': redirect_uri}
    token_response = requests.post(token_uri, data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret))
    access_tokens = json.loads(token_response.text)
    access_token = access_tokens['access_token']
    token_shelve['token'] = access_token
    token_shelve.close()

if ( access_token ):
    content = 'Access token: ' + access_token

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
```

## Get account information

Now finally we have the token we can use, and its time to try to get some data. We will try to call `https://api.sparebank1.no/personal/banking/accounts/default`. It will return a json document with information about your default account. If the call returns `Unauthorized` the script will try to go through the process of getting the key again

```python
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
```

## Refresh token
An alternative to the above is to implement use of refresh token to get a new access token. The refresh token is valid for 30 days, and can be used to get a new access token. The refresh token is used in the same way as the access token, but with the grant_type set to refresh_token

## What now?

Hey, you made it. Now you can test our open APIs for Personal Client

You can find the documentation for the APIs here: 
[Account API](https://developer.sparebank1.no/#/api/2682DF86994D4B348363BE9AC4644EFC), [Transactions API](https://developer.sparebank1.no/#/api/9858DA06FBC842699E8E73B280DAF422) and [Transfer API](https://developer.sparebank1.no/#/api/AE260B846C7C43728DFCEC6BC59D25BE)

Remember this is just a tutorial to help you get started, and it is not a well written Python application. However for any feedback or bugs feel free to contact apideveloper@sparebank1.no
