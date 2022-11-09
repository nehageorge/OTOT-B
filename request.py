import requests

url = "http://localhost:5000/index"

headers = requests.utils.default_headers()

headers.update(
    {
        'User-Agent': 'My User Agent 1.0',
    }
)

response = requests.get(url, headers=headers)
print(response.text)
