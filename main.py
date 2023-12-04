from amocrm.v2 import tokens, Lead, Pipeline, Status, manager
import json
import requests
from datetime import datetime
import csv
tokens.default_token_manager(
    client_id="c0ebf60e-502a-400d-a58a-d77293ed2e32",
    client_secret="f3laeKXpmQiHGXafyDZUmp509mGQvagjD9vkxGb9ZsqFAWSMLw2e6VE7YhoIO1gz",
    subdomain="skyspot",
    redirect_url="https://skyspot.amocrm.ru/api/v4/leads",
    storage=tokens.FileTokensStorage(),  # by default FileTokensStorage
)
# tokens.default_token_manager.init(code="def50200db7c4d34532d0e159266309ea94c4379d9463152a057a693fde575c5ec955b05959bf9a021ed812f3b5615cfa5becff5fcc1ae6e2ce7cac605bb27ebf1de458d2914f00de7ba979605d6f977408eacb4ab7d1e70571178c8ed7e323b20f8c1126ae1b5685b20e16a3d683dde3c315c37e5c4c498f1b914991c8671ac5ff4c91f2b59c54fff02acdb7aeaa2e657ef54b9588d97feadfa85027f4574746928e4b1bf812d9b68668c76ddada79c10a101c0cc780f5392aec944be2ad8a5204ca1a71781eed3941205a94878c43b732e0e0e492a26021a2256d22f32fc9f04544205ecb072916037ac144202baf8d79e45010fd1d67b57b977b37f103a000fb0656cd955c95227edc078fe87b392d1ca0b59419e65bdaa93936633a30c36796b4e761da13291cacdda255c8ac48c2364348cadd34a2edf9d6a8db6c0ec803f5cd22b15ad7a2fbb9c418096408b658d872197cd56dbdcc2e46e00e0f7a85eeea6d9d77d13df3d5f86a0b6d12fccc00244ef6444835538fab810ef1f1eb9dc814b49390a2ab29585d26e56c9b0dc199b8e0565611ecd7d7c45e12bb1acc1792f7a04b946e077e15f78dadbc3bc0c6ae1c448846e87f86ff7de0b370609841a0d4821da40ad1193138260b26091d41a1a2bf3bacfb3da8a6fac59e8f140f6ae8781c2b8bcd042243c9df45fd3b413ea63998ed2b21f7df6fc",
#                                         skip_error=False

# print(Status.get_for(Pipeline.objects.get(query='Основная воронка')).get(query='Выставлено КП'))
# for _ in Lead.objects.filter({'name':'test'}):
#     print(_)
with open('access_token.txt','r') as file:
    access_token = file.read()
headers = {"Authorization": "Bearer " +access_token}
#https://skyspot.amocrm.ru/api/v4/leads?filter[statuses][0][pipeline_id]=6733898&filter[statuses][0][status_id]=61636746
response_leads = requests.get("https://skyspot.amocrm.ru/api/v4/leads?filter[statuses][0][pipeline_id]=6733898&filter[statuses][0][status_id]=61636746",headers=headers)
dict_leads = json.loads(response_leads.text)
leads = dict_leads.get('_embedded').get('leads')
data = []
for lead in leads:
    lead_id = lead.get('id')
    price = lead.get('price')
    date = lead.get('created_at')
    date = datetime.utcfromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')
    print(date)
    response_link_lead = requests.get(f'https://skyspot.amocrm.ru/api/v4/leads/{lead_id}/links',headers=headers)
    print(json.loads(response_link_lead.text).get('_embedded').get('links'))
    if json.loads(response_link_lead.text).get('_embedded').get('links') != []:
        contact_id = json.loads(response_link_lead.text).get('_embedded').get('links')[0].get('to_entity_id')
        print(contact_id)
        response_contact = requests.get(f'https://skyspot.amocrm.ru/api/v4/contacts/{contact_id}',headers=headers)
        if response_contact.text != '':
            if json.loads(response_contact.text).get('custom_fields_values') != None:    
                for _ in json.loads(response_contact.text).get('custom_fields_values'):
                    if _.get('field_name') == 'Телефон':
                        phone = _.get('values')[0].get('value')
            elif json.loads(response_contact.text).get('values') != None:
                phone = json.loads(response_contact.text).get('values')[0].get('value')
            else:
                phone = None
    if phone != None and phone[0]=='+':
        phone = phone[1:]
    print(phone)
    data.append([date,phone,price])
with open('clientdata.csv','w', newline='') as file:
    writer = csv.writer(file)
    for line in data:
        if data[1] != None:
            writer.writerow(line)
#response_leads = requests.get("https://skyspot.amocrm.ru/api/v4/leads?filter[name]=test228",headers=headers)
#print(response_leads.text)

counter = 65652286
access_token = "y0_AgAAAABgp3QzAAruswAAAADzyagym-KsQaTdTU2G8ReWbtUdyfsjG0o&token_type"

file = open("clientdata.csv", "r").read()
id_type = "CLIENT_ID"

url = "https://api-metrika.yandex.net/cdp/api/v1/counter/65652286/data/simple_orders?merge_mode=SAVE&"
headers = {"Authorization": "Bearer " + access_token}
req = requests.post(url, headers=headers,files={"file":file})
print(req.text)