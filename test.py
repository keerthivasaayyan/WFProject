import requests
import json
t = input("")
h = requests.get(f"http://127.0.0.1:5000/check?hash={t}")
respons = h.json()
print(respons['message'])