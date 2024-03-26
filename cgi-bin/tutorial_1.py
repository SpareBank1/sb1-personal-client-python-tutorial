#!/usr/bin/env python3.7

import uuid

client_id = '<< client_id >>'
client_secret = '<< client_secret >>'
fid = '<< fid >>'

redirect_uri = "http://localhost:8000/cgi-bin/tutorial_1.py"
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