from setuptools import setup, find_packages  # , find_namespace_packages

setup(
    name='stage_testing',
    packages=find_packages(),
    # py_modules=[],
    description='Application context and related stuff',
    version='0.0.4',
    url='https://bitbucket.org/karzade/pkscan-web3-1',
    author='Sumit',
    author_email='sumit.s@karza.in',
    include_package_data=True,
    # https://pypi.org/project/deepdiff/
    # install_requires=["attrs==19.3.0", "Automat==0.8.0", "beautifulsoup4==4.8.1", "bs4==0.0.1",
    #                   "cassandra-driver==3.14.0", "certifi==2019.11.28", "cffi==1.13.2", "chardet==3.0.4",
    #                   "confluent-kafka==1.3.0", "constantly==15.1.0", "cryptography==2.8", "deepdiff==4.0.9",
    #                   "dnspython==1.16.0", "elasticsearch==6.3.1", "enum34==1.1.6", "future==0.18.2", "futures==3.1.1",
    #                   "hyperlink==19.0.0", "idna==2.8", "incremental==17.5.0", "jsonpickle==1.2", "lxml==4.4.2",
    #                   "nltk==3.3", "ordered-set==3.1.1", "pyasn1==0.4.8", "pyasn1-modules==0.2.8", "pycparser==2.19",
    #                   "PyHamcrest==1.9.0", "pymongo==3.10.0", "pyOpenSSL==19.0.0", "python-dateutil==2.8.1",
    #                   "pytz==2019.3", "repoze.lru==0.7", "requests==2.22.0", "requests-file==1.4.3", "Routes==2.4.1",
    #                   "service-identity==18.1.0", "six==1.13.0", "soupsieve==1.9.5", "tldextract==2.2.2",
    #                   "Twisted==19.10.0", "urllib3==1.25.7", "validate-email==1.3", "zope.interface==4.7.1"]
    # python3 setup.py sdist upload -r pypicloud
)
