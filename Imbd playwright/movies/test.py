import requests
import random
response = requests.get(
    url='https://headers.scrapeops.io/v1/user-agents',
    params={
        'api_key': 'bec6d2e7-aef4-44b7-a75f-84dfefdea0c6',
        'num_results': '10'}
)
responses = requests.get(
  url='https://headers.scrapeops.io/v1/browser-headers',
  params={
      'api_key': 'bec6d2e7-aef4-44b7-a75f-84dfefdea0c6',
      'num_results': '1'}
)

user_agent = response.json().get('result')
print(random.choice(user_agent))

