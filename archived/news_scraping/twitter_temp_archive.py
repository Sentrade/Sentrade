import base64
import requests
import json

#Define your keys from the developer portal
client_key = 'o62Qbz4RQcWoSlZwYAf8rk6Br'
client_secret = 'rIA9adduzHxl6lude0lCNYoyNy00trNTsGmrlHNR1M5anasaeB'
#Reformat the keys and encode them
key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')

# Transform from bytes to bytes that can be printed
b64_encoded_key = base64.b64encode(key_secret)
#Transform from bytes back into Unicode
b64_encoded_key = b64_encoded_key.decode('ascii')

base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)
auth_headers = {
    'Authorization': 'Basic {}'.format(b64_encoded_key),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}
auth_data = {
    'grant_type': 'client_credentials'
}
auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)

# print(auth_resp.status_code)

access_token = auth_resp.json()['access_token']

search_headers = {
    'Authorization': 'Bearer {}'.format(access_token)    
}
search_params = {
    'q': '#APPLE ',
    'result_type': 'recent',
    'count': 10000
}

# Create the URL
search_url = '{}1.1/search/tweets.json'.format(base_url)
# Execute the get request
search_resp = requests.get(search_url, headers=search_headers, params=search_params)
# Get the data from the request
Data = json.loads( search_resp.content )
# Print out the data!
# print(Data['statuses'])

url = 'https://api.twitter.com/1.1/application/rate_limit_status.json'
#Execute the request
search_resp = requests.get(url, headers=search_headers)
#See the remaining rate limit
json.loads(search_resp.content)['resources']['search']
# print(search_resp)

with open("temp.json", "w") as output_file:
    json.dump(Data['statuses'], output_file)
