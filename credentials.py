import base64

login = "andreas_ulrich@hotmail.com"
password = "f4203e32318d9f9c"



credentials = f"{login}:{password}"

base64_credentials = base64.b64encode(credentials.encode()).decode()

print(base64_credentials)