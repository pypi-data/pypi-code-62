from setuptools import setup

with open ("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='fpga_ethernet_control',
    version='0.0.1',
    description='Ethernet to FPGA API',
    py_modules=["wiz_scpi"],
    package_dir={'':'src'},
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'socket_control_ivie',
    ]
)