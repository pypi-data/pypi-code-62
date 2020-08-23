NAME: str = "init"
DESCRIPTION: str = """\
            Creates a Python virtual environment based on the configuration
            of an existing 'caos.yml' file in the current directory.
            
            If the 'caos.yml' file is not present in the current directory a
            new virtual environment and configuration file are created.
            
            If the '--simple' flag is used a simplified version of the 'caos.yml'
            is generated and no virtual environment is created automatically.\
"""
CLI_USAGE_EXAMPLE: str = """\
            caos init  
            caos init [VIRTUAL_ENV_NAME]
            caos init --simple | -s | -S
"""

_CAOS_YAML_TEMPLATE="""\
virtual_environment: {VENV_NAME}

dependencies:
  pip: latest
#  requests: 2.0.0  # Allow only Exact version
#  numpy: ^1.18.2 # Allow only Minor version changes
#  flask: ~1.1.0  # Allow only Patch version changes
#  flask: ./Flask-1.1.2.tar.gz # Local tar.gz package
#  tensorflow: ./local_libs/tensorflow-1.13.1-py3-none-any.whl # Local WHl package
#  tensorflow: https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.14.0-py3-none-any.whl # Remote WHl package

tasks:
  unittest:
    - echo Testing...
    - caos python -m unittest discover -v ./
#
#  start:
#    - echo Starting...
#    - caos python ./main.py
#
#  test_and_start:
#    - unittest
#    - start
"""

_CAOS_YAML_TEMPLATE_SIMPLE="""\
virtual_environment: {VENV_NAME}

dependencies:
  pip: latest

tasks:
  hello:
    - echo Hello World!
"""
