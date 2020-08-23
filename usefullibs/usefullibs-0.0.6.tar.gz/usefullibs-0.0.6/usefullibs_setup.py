from setuptools import setup, find_packages
long = """
file:
    usefullibs-|-backupzip-__init.py
               |
               |-constants-__init.py
               |
               |-cryptography-|
               |              |-affineCipher-|-affineCipher.py
               |              |              |-affineHacker.py
               |              |              |-cryptomath.py
               |              |
               |              |-caeserCipher-|-caeserCipher.py
               |              |              |-caeserHacker.py
               |              |
               |              |-publickeycipher-|-cryptomath.py
               |              |                 |-makePublicPrivateKeys
               |              |                 |-primeNum
               |              |                 |-publickeycipher
               |              |                 |-rabinMiller
               |              |
               |              |-subCipher-|-dictionary.txt
               |              |           |-makeWordPatterns.py
               |              |           |-simpleSubCipher.py
               |              |           |-simpleSubDictionaryHacker
               |              |           |-simpleSubHacker
               |              |           |wordPatterns.py
               |              |
               |              |-transpositionCipher-|-transpositionEncrypt.py
               |              |                     |-transpositionDecrypt.py
               |              |                     |-transpositionFileCipher.py
               |              |                     |-transpositionFileHacker.py
               |              |                     |-transpositionHacker.py
               |              |
               |              |-vigenereCipher-|-detectEnlish.py
               |              |                |-dictionary.txt
               |              |                |-freqAnalysis.py
               |              |                |-vigenereCipher.py
               |              |                |-vigenereDictionaryHacker.py
               |              |                |-vigenereHacker.py
               |
               |-enviroment_variables-__init__.py*
               |
               |-simple_import-__init__.py
               |
               |-socket-|-__init__.py
               |        |-exeptions.py
               |
               |-tarfile-__init__.py

(__pycache__ folders not included)
*: only works for windows\n

"""
setup(
    name="usefullibs", # Replace with your own username
    version="0.0.6",
    author="Allen Sun",
    author_email="allen.haha@hotmail.com",
    description="a useful package.",
    long_description=long,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['cryptography>=3.0', 'pyperclip>=1.8.0', 'requests>=2.24.0', 'python-whois>=0.7.3'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
