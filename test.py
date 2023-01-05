import requests

url = "https://api.apilayer.com/currency_data/live?source=EUR&currencies=RUB"

payload = {}
headers= {
  "apikey": "6g61Ns6YurAIOZRSmdWDm33wdm01vaDa"
}

response = requests.request("GET", url, headers=headers, data = payload)

status_code = response.status_code
result = response.text

print('response:\n', response, '\n')
print('result:\n', result, '\n')
print('status_code:\n', status_code, '\n')