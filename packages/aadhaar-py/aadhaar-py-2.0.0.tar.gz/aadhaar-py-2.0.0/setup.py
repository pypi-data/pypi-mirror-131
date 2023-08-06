# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aadhaar', 'aadhaar.secure_qr']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.4.0,<9.0.0', 'types-Pillow>=8.3.7,<9.0.0']

setup_kwargs = {
    'name': 'aadhaar-py',
    'version': '2.0.0',
    'description': 'Extract embedded information from Aadhaar Secure QR Code.',
    'long_description': '# aadhaar-py 🐍\n[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/aadhaar-py?color=purple)](https://pypi.org/project/aadhaar-py/)\n[![PyPI version](https://badge.fury.io/py/aadhaar-py.svg)](https://badge.fury.io/py/aadhaar-py)\n[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![codecov](https://codecov.io/gh/vishaltanwar96/aadhaar-py/branch/main/graph/badge.svg?token=JG312MQEEQ)](https://codecov.io/gh/vishaltanwar96/aadhaar-py)\n[![Downloads](https://pepy.tech/badge/aadhaar-py)](https://pepy.tech/project/aadhaar-py)\n\nThis library helps you extract the embedded information 💾 in Aadhaar Secure QR Code\n\n# Inspired from 😇\nI would like to thank the authors of [pyaadhaar](https://github.com/Tanmoy741127/pyaadhaar). It wouldn\'t be possible to move into the right direction without this library.\n\n# Demo ✔️\n[Secure Aadhaar QR Decoder](https://aadhaar-secure-qr.herokuapp.com/)\n\n# Enough talk, show me how it works! ✨\n```python\n>>> from aadhaar.secure_qr import extract_data\n>>> received_qr_code_data = 12345678\n>>> extracted_data = extract_data(received_qr_code_data)\n```\n\nThe `extract_data` function returns an instance of `ExtractedSecureQRData` which has the definition of:\n```python\n@dataclass(frozen=True)\nclass ExtractedSecureQRData:\n    text_data: ExtractedTextData\n    image: Image.Image\n    contact_info: ContactData\n```\n\n\nText Data 📝:\n```python\n>>> extracted_data.text_data\nExtractedTextData(reference_id=ReferenceId(last_four_aadhaar_digits=\'8908\', timestamp=datetime.datetime(2019, 3, 5, 15, 1, 37, 123000)), name=\'Penumarthi Venkat\', date_of_birth=datetime.date(1987, 5, 7), gender=<Gender.MALE: \'Male\'>, address=Address(care_of=\'S/O: Pattabhi Rama Rao\', district=\'East Godavari\', landmark=\'Near Siva Temple\', house=\'4-83\', location=\'Sctor-2\', pin_code=\'533016\', post_office=\'Aratlakatta\', state=\'Andhra Pradesh\', street=\'Main Road\', sub_district=\'Karapa\', vtc=\'Aratlakatta\'))\n```\n\nThe Embedded Image 🌆:\n```python\n>>> extracted_data.image\n<PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=60x60 at 0x1029CA460>\n```\n\nThe Contact Information 📧:\n```python\n>>> extracted_data.contact_info\nContactData(email=Email(hex_string=None, fourth_aadhaar_digit=\'8\'), mobile=Mobile(hex_string=\'1f31f19afc2bacbd8afb84526ae4da184a2727e8c2b1b6b9a81e4dc6b74d692a\', fourth_aadhaar_digit=\'8\'))\n```\n\nBut hey! 🙄 I want to send this data via a ReSTful API, don\'t you have something to serialize that ugly instance of `ExtractedSecureQRData`? 😩\n\n`to_dict` method to the rescue 💪\n```python\n>>> extracted_data.to_dict()\n{\n  "text_data": {\n    "reference_id": {\n      "last_four_aadhaar_digits": "8908",\n      "timestamp": "2019-03-05T15:01:37.123000"\n    },\n    "name": "Penumarthi Venkat",\n    "date_of_birth": "1987-05-07",\n    "gender": "Male",\n    "address": {\n      "care_of": "S/O: Pattabhi Rama Rao",\n      "district": "East Godavari",\n      "landmark": "Near Siva Temple",\n      "house": "4-83",\n      "location": "Sctor-2",\n      "pin_code": "533016",\n      "post_office": "Aratlakatta",\n      "state": "Andhra Pradesh",\n      "street": "Main Road",\n      "sub_district": "Karapa",\n      "vtc": "Aratlakatta"\n    }\n  },\n  "image": "data:image/jpeg;base64,/9j/4AAQSkZblahblah",\n  "contact_info": {\n    "email": {\n      "hex_string": None\n    },\n    "mobile": {\n      "hex_string": "1f31f19afc2bacbd8afb84526ae4da184a2727e8c2b1b6b9a81e4dc6b74d692a"\n    }\n  }\n}\n\n```\n\n# Run Tests 🧪\n```bash\npython -m unittest discover tests/ --verbose\n```\n',
    'author': 'Vishal Tanwar',
    'author_email': 'vishal.tanwar@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vishaltanwar96/aadhaar-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
