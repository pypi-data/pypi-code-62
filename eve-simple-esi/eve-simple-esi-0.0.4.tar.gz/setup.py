import setuptools
import os
import json


data=json.load(open("data.json","r"))
for f in data['pypi']:
    if f=="dir":
        continue
    gitFile=os.path.join(data['git']['dir'],data['git'][f])
    pypiFile=os.path.join(data['pypi']['dir'],data['pypi'][f])

    with open(gitFile,'r') as inFile:
        with open(pypiFile,'w+') as outFile:
            outFile.write(inFile.read())

data["version"]["local"]=data["version"]["local"]+1

version=data["version"]["global"]+str(data["version"]["local"])

print(version)
json.dump(data,open("data.json","w"),indent="\t")

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eve-simple-esi", # Replace with your own username
    version=version,
    author="Zorg Programming",
    author_email="dr.danio@gmail.com",
    description="The Python 3+ library for simple and fast work with https://esi.evetech.net data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/drdanio/eve-simple-esi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
