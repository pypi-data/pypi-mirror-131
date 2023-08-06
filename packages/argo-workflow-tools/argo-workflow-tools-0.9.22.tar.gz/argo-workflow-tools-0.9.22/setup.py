# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['argo_workflow_tools',
 'argo_workflow_tools.dsl',
 'argo_workflow_tools.dsl.node_properties',
 'argo_workflow_tools.dsl.parameter_builders',
 'argo_workflow_tools.dsl.utils',
 'argo_workflow_tools.exceptions',
 'argo_workflow_tools.models',
 'argo_workflow_tools.models.io',
 'argo_workflow_tools.models.io.argoproj',
 'argo_workflow_tools.models.io.argoproj.events',
 'argo_workflow_tools.models.io.argoproj.workflow',
 'argo_workflow_tools.models.io.k8s',
 'argo_workflow_tools.models.io.k8s.api',
 'argo_workflow_tools.models.io.k8s.api.core',
 'argo_workflow_tools.models.io.k8s.api.policy',
 'argo_workflow_tools.models.io.k8s.apimachinery',
 'argo_workflow_tools.models.io.k8s.apimachinery.pkg',
 'argo_workflow_tools.models.io.k8s.apimachinery.pkg.api',
 'argo_workflow_tools.models.io.k8s.apimachinery.pkg.apis',
 'argo_workflow_tools.models.io.k8s.apimachinery.pkg.apis.meta',
 'argo_workflow_tools.models.io.k8s.apimachinery.pkg.util']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.0',
 'certifi<=2021.10.8',
 'contextvars>=2.4,<3.0',
 'pydantic>=1.7.4,<2.0.0',
 'requests>=2.26.0,<3.0.0',
 'shortuuid>=1.0.8,<2.0.0',
 'urllib3<2.0.0']

setup_kwargs = {
    'name': 'argo-workflow-tools',
    'version': '0.9.22',
    'description': 'A suite of tools to ease ML pipeline development with Argo Workflows',
    'long_description': '# Argo Workflow Tools\nargo-workflow-tools is a set of tools intended to easue the usage of argo for data science and data engineerign workflows\n![Python Versions Supported](https://img.shields.io/badge/python-3.7+-blue.svg)\n\n## Installation\nargo-workflow-tools is published to the Python Package Index (PyPI) under the name argo-workflow-tools. To install it, run:\n\n``` shell\npip install argo-workflow-tools\n```\n\n## Argo Submitter\nArgo Submitter is an easy to use argo client that allows data scientists to easily execute and control Argo Workflows from code and interactive notebooks.\n\n### Quick Start\n\n#### Running workflows from templates\nThe simplest way to submit a new workflow is by running a workflow from template \n```python\nARGO_CLIENT = \'http://localhost:2746\'\nclient = ArgoClient(ARGO_CLIENT, options=ArgoOptions(client_side_validation=False, namespace=\'argo\'))\nresult = client.submit(\'test-workflow\', params={\'message\':\'hello world\'})\nresult.wait_for_completion()\n```\n\nYou can wait for template completion by setting _wait=True_ parameter, or calling wait_for_completion()\n```python\nresult = client.submit(\'test-workflow\', params={\'message\':\'hello world\'}, wait=True)\n```\n\nYou may send parameters, through the params dictionary\n```python\nresult = client.submit(\'test-workflow\', params={\'message\':\'hello world\'}, wait=True)\n```\n\nYou send objects as parameters, and they will be automatically serialized to json. \n```python\nARGO_CLIENT = \'http://localhost:2746\'\nclient = ArgoClient(ARGO_CLIENT, options=ArgoOptions(client_side_validation=False, namespace=\'argo\'))\nresult = client.submit(\'test-workflow\',\n                                     params={\'name\':\n                                                {\'first\':\'Lorne\',\'last\':\'Malvo\'}\n                                             },\n                                     wait=True)\n```\n#### Running workflows from specification\nif you have a custom workflow manifest , you can run it by using _create_\n```python\nresult = client.create(workflow_manifest, wait=True)\n```\n#### Working with workflow results\nYou can check the status of a workflow by calling the status field\n```python\nresult.status\n```\n\nYou can fetch output parametes and artifacts throut the output field\n```python\nprint(result.outputs[\'message\'])\n```\nAs well as reach artifacts through the s3 path property\n```python\npandas.read_csv(result.outputs[\'users\'].s3)\n```\n#### Controlling workflows\nYou may cancel a running flow through the cancel method\n```python\nresult.cancel()\n```\nYou may ssuspend, resume or cancel your workflow at any time \n```python\nresult = client.submit(\'test-workflow\', params={\'message\':\'hello world\'}, wait=False)\nresult.suspend()\n...\nresult.resume()\n```\nYou can retry a failing workflow through the retry method\n```python\nresult.retry()\n```\n\n## Pythonic workflow DSL\n\nFargo is a library for autoring Argo Workflows in a Python and friendly way. The main goal of Hera are\n* Make Argo Workflows accessible by leveraging pythonic style of dag\n* Allow seamlless local runs, for debug or testing while maintaining the same codebase for running DAG\'s at scale\n\npythonic DSL is an opinionate subset of writing Argo workflows, it favors simplicity, readability and "pythonic flow" over leveraging the entire capability set Argo Workflows brings. \n\n### Concepts\n* task - atomic python code\n* DAG - atonic workflows code\n\n### Quick start\n\n####Hello World\n```python\n\ndef say_hello(name):\n    message = f"hello {name}"\n    print(message)\n    return message\n\nsay_hello("Brian")\n\n```\nto run this simple task in argo all we need to do is to decorate our code in a task decorator\n\n```python\n@dsl.Task(image="python3:3.10")\ndef say_hello(name:str):\n    message = f"hello {name}"\n    print(message)\n    return message\n\n\nworkflow = Workflow(name="hello-world", entrypoint=say_hello, arguments={"name": "Brian"})\nprint(workflow.to_yaml())\n\n```\n#### DAG\nDAG functions are functions that define a workflow by calling other tasks or nested DAGs, \nWe support task depndency declaration implicitly by analyzing inputs and outputs of each task. \n\nWhen writing DAG functions make sure you keep it a simple as possible, call only DAG or TASK flows.\n\n```python\n@dsl.Task(image="python:3.10")\ndef multiply_task(x: int):\n    return x * 2\n\n\n@dsl.Task(image="python:3.10")\ndef sum_task(x: int, y: int):\n    return x + y\n\n\n@dsl.DAG()\ndef diamond(num: int):\n    a = multiply_task(num)\n    b = multiply_task(a)\n    c = multiply_task(num)\n    return sum_task(b, c)\n\n ```\n\n#### Explicit depndencies \nIn case a task does not return a parameter, you can set an explicit dependency by sending wait_for argument to the next task\n```python\n@dsl.Task(image="python:3.10")\ndef print_task():\n    print(f"text")\n\n\n@dsl.DAG()\ndef diamond():\n    a = print_task()\n    b = print_task(wait_for=a)\n    c = print_task(wait_for=a)\n    print_task(wait_for=[c, b])\n\n```\n\n#### Loops\nwe support map reduce workflows through ```[for in]``` loop, the iterable input must be a parameter, an output of a previous task, or a sequence object. \n\ncurrently only one level of nesting is supported, in case you wish to use nested loops, extract the second loop into a fucntion and decorate it as well with a DAG decorater.\n```python\n@dsl.Task(image="python:3.10")\ndef generate_list(partitions: int, partition_size: int):\n    items = []\n    for i in range(partitions):\n        items.append(list(range(1, partition_size)))\n\n    return items\n\n\n@dsl.Task(image="python:3.10")\ndef sum_task(items:list[int]):\n    return sum(items)\n\n\n@dsl.DAG()\ndef map_reduce(partitions, partition_size):\n    partition_list = generate_list(partitions, partition_size)\n    partition_sums = [sum_task(partition) for partition in partition_list]\n    return sum_task(partition_sums)\n```\n\n#### Conditions \nwe support conditional task run by employing the \'with condition\' syntax\n\n```python\n    @Task(image="python:3.10")\n    def say_hello(name: str):\n        message = f"hello {name}"\n        print(message)\n        return message\n    \n    @Task(image="python:3.10")\n    def say_goodbye(name: str):\n        message = f"goodbye {name}"\n        print(message)\n        return message\n\n\n    @DAG()\n    def command_hello(name, command):\n        with Condition().equals(command, "hello"):\n            say_hello(name)\n        with Condition().equals(command, "goodbye"):\n            say_goodbye(name)\n```\n\n## How to contribute\n\nHave any feedback? Wish to implement an extenstion or new capability? Want to help us make argo better and easier to use?\nEvery contribution to _Argo Workflow Tools_ is greatly appreciated.\n\n',
    'author': 'Diagnostic Robotics',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DiagnosticRobotics/argo-workflow-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
