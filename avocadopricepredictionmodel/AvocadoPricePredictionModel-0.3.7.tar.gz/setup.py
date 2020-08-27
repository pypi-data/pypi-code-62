from setuptools import setup, find_packages

setup(
    name='AvocadoPricePredictionModel',
    version='0.3.7',
    packages=["PricePredictionModel"],
    include_package_data=True,
    package_data={
        "PricePredictionModel": ["model.pkl"],
    },
    install_requires=["scikit-learn", "threadpoolctl"],
    url='https://github.com/NadavAtGitHub/AvocadoPricePrediction',
    license='GPL3',
    author='Nadav Donner',
    author_email='nadavdonner@idf.il',
    description='A model to predict avocado prices!'
)

