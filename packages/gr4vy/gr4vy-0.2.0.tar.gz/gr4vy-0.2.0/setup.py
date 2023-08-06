# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gr4vy',
 'gr4vy.gr4vy_api.openapi_client',
 'gr4vy.gr4vy_api.openapi_client.api',
 'gr4vy.gr4vy_api.openapi_client.apis',
 'gr4vy.gr4vy_api.openapi_client.model',
 'gr4vy.gr4vy_api.openapi_client.models',
 'gr4vy.gr4vy_api.openapi_client.test']

package_data = \
{'': ['*'],
 'gr4vy': ['gr4vy_api/*', 'gr4vy_api/.openapi-generator/*'],
 'gr4vy.gr4vy_api.openapi_client': ['docs/*']}

install_requires = \
['DateTime>=4.3,<5.0',
 'PyJWT>=2.3.0,<3.0.0',
 'certifi>=2021.10.8,<2022.0.0',
 'cryptography>=3.4.6,<4.0.0',
 'pem>=21.2.0,<22.0.0',
 'pyOpenSSL>=21.0.0,<22.0.0',
 'pycryptodome>=3.11.0,<4.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'python-jose[cryptography]>=3.2.0,<4.0.0',
 'six>=1.16.0,<2.0.0',
 'urllib3>=1.26.5,<2.0.0']

setup_kwargs = {
    'name': 'gr4vy',
    'version': '0.2.0',
    'description': 'Python SDK for Gr4vy',
    'long_description': '# Gr4vy SDK for Python\n\nGr4vy provides any of your payment integrations through one unified API. For\nmore details, visit [gr4vy.com](https://gr4vy.com).\n\n## Installation\n\nTo add Gr4vy to your project simply install with pip:\n\n```python\npip install gr4vy\n```\n\nAdd import:\n\n```python\nimport gr4vy\n```\n\n## Getting Started\n\nTo make your first API call, you will need to [request](https://gr4vy.com) a\nGr4vy instance to be set up. Please contact our sales team for a demo.\n\nOnce you have been set up with a Gr4vy account you will need to head over to the\n**Integrations** panel and generate a private key. We recommend storing this key\nin a secure location but in this code sample we simply read the file from disk.\n\n```python\nfrom gr4vy import Gr4vyClient\nclient = Gr4vyClient("gr4vy_instance","location_of_key_file", "sandbox_or_production")\nclient.ListBuyers()\n\n```\n\n## Gr4vy Embed\n\nTo create a token for Gr4vy Embed, call the `client.GetEmbedToken(embed)`\nfunction with the amount, currency, and optional buyer information for Gr4vy\nEmbed.\n\n```python\nembed = {\n  "amount": 1299,\n  "currency": "USD",\n  "buyerExternalIdentifier": "user-12345",\n}\n\ntoken = client.GenerateEmbedToken(embed)\n```\n\nYou can now pass this token to your frontend where it can be used to\nauthenticate Gr4vy Embed.\n\nThe `buyer_id` and/or `buyer_external_identifier` fields can be used to allow\nthe token to pull in previously stored payment methods for a user. A buyer\nneeds to be created before it can be used in this way.\n\n```python\n  from gr4vy import Gr4vyClient\n  from gr4vy import BuyerRequest\n  client = Gr4vyClient("gr4vy_instance","private_key.pem", "production")\n\n  buyer_request = BuyerRequest(display_name = "Jane Smith")\n\n  new_buyer = client.AddBuyer(buyer_request)\n\n  embed = {\n    "amount": 1299,\n    "currency": "USD",\n    "buyerId": new_buyer.id,\n  }\n\n  embed_token = client.GenerateEmbedToken(embed)\n\n  print("Embed token: {}".format(embed_token))\n```\n\n## Initialization\n\nThe client can be initialized with the Gr4vy ID (`gr4vyId`), the location of the private key, and the environment attempting to access.\n\n```python\n  client = Gr4vyClient("gr4vyId","private_key.pem", "sandbox")\n```\n\nAlternatively, instead of the `gr4vyId` it can be initialized with the `baseUrl`\nof the server to use directly and the environment attempting to acess .\n\n```python\n  client = Gr4vyClientWithBaseUrl("https://*gr4vyId*.gr4vy.app","private_key.pem", "sandbox")\n```\n\nYour API private key can be created in your admin panel on the **Integrations**\ntab.\n\n\n## Making API calls\n\nThis library conveniently maps every API path to a seperate function. For\nexample, `GET /buyers?limit=100` would be:\n\n```python\n  client.ListBuyers(2)\n```\n\nTo create, the API requires a request object for that resource that is conventiently\nnamed `Gr4vy<Resource>Request`.  To update, the API requires a request object\nfor that resource that is named `Gr4vy<Resource>Update`.\n\nFor example, to create a buyer you will need to pass a `Gr4vyBuyerRequest` object to\nthe `AddBuyer` method.\n\n```python\n  from gr4vy import BuyerRequest\n\n  buyer_request = BuyerRequest(display_name = "Jane Smith")\n  new_buyer = client.AddBuyer(buyer_request)\n\n```\n\nSo to update a buyer you will need to pass in the `Gr4vyBuyerUpdate` to the\n`UpdateBuyer` method.\n\n```python\n  buyer_request = BuyerUpdate(display_name = "Jane Changed")\n  buyer_update = client.UpdateBuyer(buyer_id, buyer_request)\n```\n\n## Response\n\nEvery resolved API call returns the requested resource, errors are printed to the console\n\n\n```python\n  print(client.ListBuyers())\n```\n\n## Logging & Debugging\n\nThe SDK makes it easy possible to log responses to the console.\n\n```python\n  print(client.ListBuyers())\n```\n\nThis will output the request parameters and response to the console as follows.\n\n```sh\n{"items":[{"id":"b8433347-a16f-46b5-958f-d681876546a6","type":"buyer","display_name":"Jane Smith","external_identifier":None,"created_at":"2021-04-22T06:51:16.910297+00:00","updated_at":"2021-04-22T07:18:49.816242+00:00"}],"limit":1,"next_cursor":"fAA0YjY5NmU2My00NzY5LTQ2OGMtOTEyNC0xODVjMDdjZTY5MzEAMjAyMS0wNC0yMlQwNjozNTowNy4yNTMxMDY","previous_cursor":None}\n```\n\n## Development\n\n### Adding new APIs\n\nTo add new APIs, run the following command to update the models and APIs based\non the API spec.\n\n```sh\n./openapi-generator-generate.sh\n```\n\nRun the tests to ensure the changes do not break any existing tests. Using PyTest. In `test_gr4vy.py` update the following lines with your Gr4vy ID and the location of the private key file.\n\n```python\ngr4vy_id = "YOUR_GR4VY_ID"\nprivate_key_location = "PRIVATE_KEY_LOCATION"\n```\n\n```sh\npytest -v\n```\n\n### Publishing\n\nThis project is published to PyPi.\n\n## License\n\nThis library is released under the [MIT License](LICENSE).\n',
    'author': 'Gr4vy',
    'author_email': 'code@gr4vy.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
