# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stargql']

package_data = \
{'': ['*']}

install_requires = \
['python-gql>=0.1', 'starlette>0.13']

setup_kwargs = {
    'name': 'starlette-graphql',
    'version': '0.1.4',
    'description': 'The starlette GraphQL implement, which  support query, mutate and subscription.',
    'long_description': '# Starlette GraphQL\n\nThe starlette GraphQL implement, which  support query, mutate and subscription. Based on [python-gql](https://github.com/syfun/python-gql).\n\n## Requirement\n\nPython 3.7+\n\n## Installation\n\n`pip install starlette-graphql`\n\n\n## Getting started\n\n```python\n# app.py\nfrom gql import query, gql\nfrom stargql import GraphQL\n\ntype_defs = gql("""\ntype Query {\n    hello(name: String!): String!\n}\n""")\n\n\n@query\nasync def hello(parent, info, name: str) -> str:\n    return name\n\n\napp = GraphQL(type_defs=type_defs)\n```\n\nUse [uvicorn](https://www.uvicorn.org) to run app.\n\n`uvicorn app:app --reload`\n\n## Upload File\n\n```python\nimport uvicorn\nfrom gql import gql, mutate\nfrom stargql import GraphQL\n\ntype_defs = gql("""\n scalar Upload\n \n type File {\n    filename: String!\n  }\n\n  type Query {\n    uploads: [File]\n  }\n\n  type Mutation {\n    singleUpload(file: Upload!): File!\n    multiUpload(files: [Upload!]!): [File!]!\n  }\n""")\n\n\n@mutate\ndef single_upload(parent, info, file):\n    return file\n\n\n@mutate\ndef multi_upload(parent, info, files):\n    return files\n\n\napp = GraphQL(type_defs=type_defs)\n\n\nif __name__ == \'__main__\':\n    uvicorn.run(app, port=8080)\n\n```\n\n## Subscription\n\nFor more about subscription, please see [gql-subscriptions](https://github.com/syfun/starlette-graphql).\n\n## Apollo Federation\n\n[Example](https://github.com/syfun/starlette-graphql/tree/master/examples/federation)\n\nFor more abount subscription, please see [Apollo Federation](https://www.apollographql.com/docs/apollo-server/federation/introduction/)\n',
    'author': 'syfun',
    'author_email': 'sunyu418@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/syfun/starlette-graphql',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.7',
}


setup(**setup_kwargs)
