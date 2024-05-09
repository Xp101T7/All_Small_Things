from google.oauth2 import id_token
from google.auth.transport import requests

# Replace 'your_token' with your actual JWT
token = 'your_token'
request = requests.Request()

# This will raise an exception if the token is invalid
try:
    id_info = id_token.verify_oauth2_token(token, request)
    print(id_info)
except ValueError as error:
    print(error)
