# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djangomockingbird']

package_data = \
{'': ['*']}

install_requires = \
['black>=21.11b1,<22.0', 'django>=2.2,<3.0']

setup_kwargs = {
    'name': 'djangomockingbird',
    'version': '1.0.8',
    'description': 'The fastest way to write the fastest Django unit tests',
    'long_description': "\n\n# Django Mockingbird: the fastest way to write the fastest Django unit tests\n\n\n![GitHub](https://img.shields.io/github/license/larsvonschaff/Django-mockingbird)\n![PyPI](https://img.shields.io/pypi/v/djangomockingbird)\n\n\n\n## 1. What is Django Mockingbird and why would I need it?\n\nUntil now, there were two options for writing tests for a Django application: either create objects in the database for every test or mock the database queries using [Unit test’s Mock](https://docs.python.org/3/library/unittest.mock.html). While the former is slow, the latter is complicated to write and read. Both add a lot of setup code to our tests. Django Mockingbird introduces a new way to write tests for Django, which is fast to run as well as simple to write.\n\n## 2. How does it work?\n\nIt works by creating a mock object which behaves exactly like the Django model, but does not execute any queries under the hood. It only takes one line of code to use it in your test. It is not meant to be used in place of frameworks like [Pytest](https://docs.pytest.org/en/6.2.x/), but to complement them.\n\n## 3. How do I use it?\n\n### Installation \n\n```python\npip install djangomockingbird\n```\n\n### Usage\n\n```python\n\nfrom djangomockingbird import mock_model\n\n@mock_model('myapp.myfile.MyModel')\ndef test_my_test():\n    some_test_query = MyModel.objects.filter(bar='bar').filter.(foo='foo').first()\n    #some more code\n    #assertions here\n\n```\nWith the mock_model decorator this test will pass no matter how complicated the query and will never touch the database.\n\n\n### Specifiying mock return data\n\nYou can specify the values of specific fields of the model object you are mocking. If you don’t empty strings will be returned. Construct a dictionary with field names as keys and desired returs as values and pass it to the 'specs' argument of make_mocks. If you try to specify a nonexisant field as a key an error will be thrown, but you can specify any kind of value you want.\n\n```python\n\n@mock_model('myapp.myfile.MyModel', specs={'field': 'value'})\n\n```\n\n### Attention! Cases where returns must be specified: Model methods\n\nIf your model has custom methods and they are used by the test, you must specify their names and return data to the mock, otherwise your tests won't pass. \n\n```python\n\n model_method_specs = {'to_dict': {'': ''}}\n@mock_model('myapp.myfile.MyModel', model_method_specs=model_method_specs)\n \n ```\n\n\n## 4. Is it production ready? Can I help make it better? \n\nThis is still a very new project, but is quite stable for the general use case. However, there are advanced use cases that are not yet supported, most notably [custom model managers](https://docs.djangoproject.com/en/3.1/topics/db/managers/#custom-managers). For those test cases you can try supplementing Django Mockingbird with your own code or other libraries. Because this tool is really just one elaborate mock model it is very flexible and plays well with pretty much anything.\n\nWe would appreciate you opening issues to bring any defects or oversights to light. Contributions are also kindly accepted - see more on the code arhitecture principles below if you are interested. \n\n## 5. Where can I read more details on the architecture?\n\nRead about the how functional programming principles were used in the library [here](http://www.cmdctrlesc.xyz/post/6) and on metaprogramming features [here](http://www.cmdctrlesc.xyz/post/5).\n\n\n\n\n\n\n\n",
    'author': 'larsvonschaff',
    'author_email': 'larsvonschaff@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/larsvonschaff/Django-mockingbird',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
