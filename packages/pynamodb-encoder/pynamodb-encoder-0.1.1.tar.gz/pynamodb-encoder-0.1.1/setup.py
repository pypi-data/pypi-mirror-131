# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pynamodb_encoder']

package_data = \
{'': ['*']}

install_requires = \
['pynamodb>=5.1.0,<6.0.0']

setup_kwargs = {
    'name': 'pynamodb-encoder',
    'version': '0.1.1',
    'description': 'Helper classes that encode/decode pynamodb models to/from JSON serializable dict',
    'long_description': '# pynamodb-encoder\n![Build](https://github.com/lyang/pynamodb-encoder/actions/workflows/build.yml/badge.svg) ![CodeQL](https://github.com/lyang/pynamodb-encoder/actions/workflows/codeql-analysis.yml/badge.svg) [![codecov](https://codecov.io/gh/lyang/pynamodb-encoder/branch/main/graph/badge.svg?token=P51YVL86N8)](https://codecov.io/gh/lyang/pynamodb-encoder) [![Maintainability](https://api.codeclimate.com/v1/badges/1e5c3b615dedb2bffb0c/maintainability)](https://codeclimate.com/github/lyang/pynamodb-encoder/maintainability) [![PyPI version](https://badge.fury.io/py/pynamodb-encoder.svg)](https://badge.fury.io/py/pynamo-encoder)\n[![PyPI Supported Python Versions](https://img.shields.io/pypi/pyversions/pynamodb-encoder.svg)](https://pypi.python.org/pypi/pynamodb-encoder/)\n\n## Introduction\n`pynamodb-encoder` provides helper classes that can convert [PynamoDB](https://github.com/pynamodb/PynamoDB) `Model` objects into `JSON` serializable `dict`. It can also decode such `dict` back into those `Model` objects. [Polymorphic](https://pynamodb.readthedocs.io/en/latest/polymorphism.html) models and attributes are also supported.\n\n## Examples\n```python\ndef test_encode_complex_model(encoder: Encoder):\n    class Pet(DynamicMapAttribute):\n        cls = DiscriminatorAttribute()\n        name = UnicodeAttribute()\n\n    class Cat(Pet, discriminator="Cat"):\n        pass\n\n    class Dog(Pet, discriminator="Dog"):\n        pass\n\n    class Human(Model):\n        name = UnicodeAttribute()\n        pets = ListAttribute(of=Pet)\n\n    jon = Human(name="Jon", pets=[Cat(name="Garfield", age=43), Dog(name="Odie")])\n    assert encoder.encode(jon) == {\n        "name": "Jon",\n        "pets": [{"cls": "Cat", "name": "Garfield", "age": 43}, {"cls": "Dog", "name": "Odie"}],\n    }\n\ndef test_decode_complex_model(decoder: Decoder):\n    class Pet(DynamicMapAttribute):\n        cls = DiscriminatorAttribute()\n\n    class Cat(Pet, discriminator="Cat"):\n        name = UnicodeAttribute()\n\n    class Dog(Pet, discriminator="Dog"):\n        breed = UnicodeAttribute()\n\n    class Human(Model):\n        name = UnicodeAttribute()\n        age = NumberAttribute()\n        pets = ListAttribute(of=Pet)\n\n    jon = decoder.decode(\n        Human,\n        {\n            "name": "Jon",\n            "age": 70,\n            "pets": [{"cls": "Cat", "name": "Garfield"}, {"cls": "Dog", "breed": "Terrier"}],\n        },\n    )\n\n    assert jon.name == "Jon"\n    assert jon.age == 70\n    assert isinstance(jon.pets, list)\n    assert len(jon.pets) == 2\n    assert isinstance(jon.pets[0], Cat)\n    assert jon.pets[0].name == "Garfield"\n    assert isinstance(jon.pets[1], Dog)\n    assert jon.pets[1].breed == "Terrier"\n```\n\nMore examples can be found in [encoder_test.py](tests/encoder_test.py) and [decoder_test.py](tests/decoder_test.py)\n',
    'author': 'Lin Yang',
    'author_email': 'github@linyang.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lyang/pynamodb-encoder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
