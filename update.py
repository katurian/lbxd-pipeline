import hashlib
import hmac
import json
import logging
import os
import time
from time import sleep
import uuid
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

apikey = 'f6e5971115ec9XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
apisecret = 'ea38a8c9fdXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
username = 'pybot'
password = 'password'

def generateToken(username, password):
    nonce = uuid.uuid4()
    timestamp = int(time.time())
    method = "POST"
    url = f'https://api.letterboxd.com/api/v0/auth/token?apikey={apikey}&nonce={nonce}&timestamp={timestamp}'
    body = f'grant_type=password&username={username}&password={password}'
    bytestring = b"\x00".join(
        [str.encode(method), str.encode(url), str.encode(body)]
    )
    signature = hmac.new(
        str.encode(apisecret), bytestring, digestmod=hashlib.sha256
    )
    signature = signature.hexdigest()
    r = requests.post(f'https://api.letterboxd.com/api/v0/auth/token?apikey={apikey}&nonce={nonce}&timestamp={timestamp}&signature={signature}', headers={'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'}, data=f'grant_type=password&username={username}&password={password}', verify=False)
    resultJSON = r.json()
    accesstoken = resultJSON['access_token']
    refreshtoken = resultJSON['refresh_token']
    tokens = [accesstoken, refreshtoken]
    return tokens

def refreshToken():
    nonce = uuid.uuid4()
    timestamp = int(time.time())
    method = "POST"
    url = f'https://api.letterboxd.com/api/v0/auth/token?apikey={apikey}&nonce={nonce}&timestamp={timestamp}'
    body = f'grant_type=refresh_token&refresh_token={refreshtoken}'
    bytestring = b"\x00".join(
        [str.encode(method), str.encode(url), str.encode(body)]
    )
    signature = hmac.new(
        str.encode(apisecret), bytestring, digestmod=hashlib.sha256
    )
    signature = signature.hexdigest()
    r = requests.post(f'https://api.letterboxd.com/api/v0/auth/token?apikey={apikey}&nonce={nonce}&timestamp={timestamp}&signature={signature}', headers={'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'}, data=f'grant_type=refresh_token&refresh_token={refreshtoken}', verify=False)
    resultJSON = r.json()
    return resultJSON

def default(obj):
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()

def getReviewsByTag(tagger, query):
    query = query.replace(" ", "%20")
    nonce = uuid.uuid4()
    timestamp = int(time.time())
    method = "GET"
    url = f'https://api.letterboxd.com/api/v0/log-entries?tagger={tagger}&sort=WhenAdded&where=HasReview&includeTaggerFriends=None&tagCode={query}&perPage=300&apikey={apikey}&nonce={nonce}&timestamp={timestamp}'
    bytestring = b"\x00".join(
        [str.encode(method), str.encode(url), str.encode("")]
    )
    signature = hmac.new(
        str.encode(apisecret), bytestring, digestmod=hashlib.sha256
    )
    signature = signature.hexdigest()
    
    r = requests.get(f'https://api.letterboxd.com/api/v0/log-entries?tagger={tagger}&sort=WhenAdded&where=HasReview&includeTaggerFriends=None&tagCode={query}&perPage=300&apikey={apikey}&nonce={nonce}&timestamp={timestamp}&signature={signature}', verify=False)
    resultJSON = r.json()
    return resultJSON['items']

tokens = generateToken(username, password)
bearertoken = "Bearer " + tokens[0]
refreshtoken = tokens[1]

state = False
while state == False:
    reviews = getReviewsByTag('Tqhj', 'katski-writes')
    data = json.dumps(reviews, default=default)
    os.remove('reviews.js')
    with open('reviews.js', 'w') as file:
        file.write('export default')
        file.write(data)
    sleep(15)











