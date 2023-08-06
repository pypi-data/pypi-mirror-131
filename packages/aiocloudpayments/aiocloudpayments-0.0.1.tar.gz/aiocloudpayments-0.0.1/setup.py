# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiocloudpayments',
 'aiocloudpayments.client',
 'aiocloudpayments.endpoints',
 'aiocloudpayments.endpoints.applepay',
 'aiocloudpayments.endpoints.notifications',
 'aiocloudpayments.endpoints.orders',
 'aiocloudpayments.endpoints.payments',
 'aiocloudpayments.endpoints.payments.cards',
 'aiocloudpayments.endpoints.payments.tokens',
 'aiocloudpayments.endpoints.subscriptions',
 'aiocloudpayments.types',
 'aiocloudpayments.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'aiocloudpayments',
    'version': '0.0.1',
    'description': 'CloudPayments Python Async Library',
    'long_description': '# aiocloudpayments\nPython Async [CloudPayments](https://developers.cloudpayments.ru/#api) Library\n# Basic Usage Example\n```\nfrom datetime import date\n\nfrom aiocloudpayments import AioCpClient\n\n\nasync def main():\n    client = AioCpClient(PUBLIC_ID, API_SECRET)\n\n    await client.test()\n\n    await client.charge_card(\n        amount=10,\n        currency="RUB",\n        invoice_id="1234567",\n        ip_address="123.123.123.123",\n        description="Payment for goods in example.com",\n        account_id="user_x",\n        name="CARDHOLDER NAME",\n        card_cryptogram_packet="01492500008719030128SMfLeYdKp5dSQVIiO5l6ZCJiPdel4uDjdFTTz1UnXY+3QaZcNOW8lmXg0H670MclS4lI+qLkujKF4pR5Ri+T/E04Ufq3t5ntMUVLuZ998DLm+OVHV7FxIGR7snckpg47A73v7/y88Q5dxxvVZtDVi0qCcJAiZrgKLyLCqypnMfhjsgCEPF6d4OMzkgNQiynZvKysI2q+xc9cL0+CMmQTUPytnxX52k9qLNZ55cnE8kuLvqSK+TOG7Fz03moGcVvbb9XTg1oTDL4pl9rgkG3XvvTJOwol3JDxL1i6x+VpaRxpLJg0Zd9/9xRJOBMGmwAxo8/xyvGuAj85sxLJL6fA==",\n        payer=Person(\n            first_name="Test",\n            last_name="Test",\n            middle_name="Test",\n            birth=date(1998, 1, 16),\n            address="12A, 123",\n            street="Test Avenue",\n            city="LosTestels, City of Test Angels",\n            country="Testland",\n            phone="+1 111 11 11",\n            post_code="101011010"\n        )\n    )\n\n    await client.disconnect()\n```\n\narchitecture inspired by [aiogram](https://github.com/aiogram/aiogram)',
    'author': 'drforse',
    'author_email': 'george.lifeslice@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/drforse/aiocloudpayments',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
