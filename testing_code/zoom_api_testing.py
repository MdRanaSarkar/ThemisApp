import datetime
from time import time
from django import http
import jwt

ZOOM_API_KEY = "amEtAmG9SK2FAidkZCkgDA"
ZOOM_API_SECRET = "DZpquK0GVaojqTwnALdjI3xE5HHMc7L6"


# payload = {'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=300),
#            'iss': ZOOM_API_KEY    
#           }
# token = jwt.encode(payload, ZOOM_API_SECRET).decode("utf-8")

# conn = http.client.HTTPSConnection("api.zoom.us")

def generateToken():
    token = jwt.encode(
 
        # Create a payload of the token containing
        # API Key & expiration time
        {'iss': ZOOM_API_KEY, 'exp': time() + 5000},
 
        # Secret used to generate token signature
        ZOOM_API_SECRET,
 
        # Specify the hashing alg
        algorithm='HS256'
    )
    return token.decode('utf-8')
 
print(generateToken())