import base64

username = 'andreas_ulrich@hotmail.com'
password = "f4203e32318d9f9c"

userpass = username + ':' + password
encoded_u = base64.b64encode(userpass.encode()).decode()
headers = {"Authorization" : "Basic %s" % encoded_u}