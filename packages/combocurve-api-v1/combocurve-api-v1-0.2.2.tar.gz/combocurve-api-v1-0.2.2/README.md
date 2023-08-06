# ComboCurve client for Python

## Authorization

`combocurve_api` requires the API key and service account provided by Inside Petroleum, as shown in the example below:

```python
from combocurve_api_v1 import ServiceAccount, ComboCurveAuth

# Use this to create your service account manually
service_account = ServiceAccount(
    client_email='YOUR_CLIENT_EMAIL',
    client_id='YOUR_CLIENT_ID',
    private_key='YOUR_PRIVATE_KEY',
    private_key_id='YOUR_PRIVATE_KEY_id'
)
# Or use this to load it from a JSON file
# service_account = ServiceAccount.from_file("PATH_TO_JSON_FILE")

# Set your API key
api_key = 'YOUR_API_KEY'

combocurve_auth = ComboCurveAuth(service_account, api_key)

# Get auth headers
auth_headers = combocurve_auth.get_auth_headers()
```

`combocurve_auth.get_auth_headers()` should be called before every request so that the token can be
refreshed if it's about to expire. After getting the authentication headers, they can be used with any HTTP client
library. Below is an example with the popular [Requests](https://docs.python-requests.org) library:

```python
import requests

data = [{
    'wellName': 'well 1',
    'dataSource': 'internal',
    'chosenId': '1234'
}, {
    'wellName': 'well 2',
    'dataSource': 'internal',
    'chosenId': '4321'
}]
auth_headers = combocurve_auth.get_auth_headers()
url = 'https://api.combocurve.com/v1/wells'

response = requests.put(url, headers=auth_headers, json=data)
print(response.json())
```

ComboCurve API only accepts JSON data, so it's important to make sure that the data is serialized as such, and that the
`Content-Type` header is set to `application/json`. Luckily, when using Requests it will take care of both things when
the data is passed using the `json` parameter, as shown in the example above. In other words, the line of sending the
request in that example is roughly equivalent to this:

```python
import json

response = requests.put(url,
                        headers={
                            **auth_headers, 'Content-Type': 'application/json'
                        },
                        data=json.dumps(data))
```

More information here: https://docs.python-requests.org/en/latest/user/quickstart/#more-complicated-post-requests
