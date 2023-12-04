import requests 
counter = '65652286'
token = "y0_AgAAAABgp3QzAAruswAAAADzyagym-KsQaTdTU2G8ReWbtUdyfsjG0o"

file = open("clientdata.csv", "r").read()
id_type = "CLIENT_ID"

url = "https://api-metrika.yandex.net/cdp/api/v1/counter/65652286/data/simple_orders?merge_mode=SAVE&"
headers = {git 
 "Authorization": "OAuth " + token
}
req = requests.post(url, headers=headers,files={"file":file})
print(req.text)