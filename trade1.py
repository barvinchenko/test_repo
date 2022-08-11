
import json
from datetime import datetime
import requests
from nacl.bindings import crypto_sign
import psycopg2
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import time



# replace with your api keys
public_key = "3fabf6c61fb9eb576705739954d88e9adf13864154ce0ef6679625b3005c93b1"
secret_key = "bc24f73bdeda1a6ae707cffd28e595416f2e6242696fd4d221912a60d0f0f34b3fabf6c61fb9eb576705739954d88e9adf13864154ce0ef6679625b3005c93b1"

# change url to prod
rootApiUrl = "https://api.dmarket.com"


def get_price_from_market():
    #market_response = requests.get(rootApiUrl + "/price-aggregator/v1/aggregated-prices?Titles=Artificer's Chisel&Limit=100")
    market_response = requests.get(rootApiUrl + "/exchange/v1/market/items?GameId=9a92&limit=1&currency=USD")
    offers = json.loads(market_response.text)["objects"]
    return offers


# def build_target_body_from_offer(offer):
#     print(offer)
#     return {"Targets": [
#         {"Amount": 1, "GameID": "a8db", "Price": {"Amount": 0.02, "Currency": "USD"},
#          "Attributes": [{"Name":"GameID","Value":"a8db"},{"Name":"title","Value":"Recoil Case"}    ]
#                        }    ]
#             }
def build_target_body_from_offer1():
    return {  "GameID": "9a92",
    "Targets": [
        {"Amount": 1, "GameID": "9a92", "Price": {"Amount": 0.27, "Currency": "USD"},
         "Attributes": [{"Name":"GameID","Value":"9a92"},{"Name":"title","Value":"Artificer's Hammer"}    ]
                       }    ]
            }
  


nonce = str(round(datetime.now().timestamp()))
api_url_path = "/marketplace-api/v1/user-targets/create"
method = "POST"
#offer_from_market = get_price_from_market()
#print(offer_from_market)
#
body = build_target_body_from_offer1()
#
string_to_sign = method + api_url_path + json.dumps(body) + nonce
signature_prefix = "dmar ed25519 "
encoded = string_to_sign.encode('utf-8')
secret_bytes = bytes.fromhex(secret_key)
signature_bytes = crypto_sign(encoded, bytes.fromhex(secret_key))
signature = signature_bytes[:64].hex()
headers = {
     "X-Api-Key": public_key,
     "X-Request-Sign": signature_prefix + signature,
     "X-Sign-Date": nonce
 }

resp = requests.post(rootApiUrl + api_url_path, json=body, headers=headers)
print(resp.text)
