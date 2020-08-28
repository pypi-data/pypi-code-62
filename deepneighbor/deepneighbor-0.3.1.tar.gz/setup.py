import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
REQUIRED_PACKAGES = [
    'h5py',
    'requests',
    'gensim==3.7.0',
    'tqdm',
    'numpy',
    'scikit-learn',
    'pandas',
    'annoy',
    'dgl',
    'torch>=1.1.0',
    'tqdm'

]

setuptools.setup(

  name="deepneighbor",
  version="0.3.1",
  author="Yufeng Wang",
  author_email="louiswang524@gmail.com",
  description="embedding-based item nearest neighborhoods extraction",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/LouisBIGDATA/deepneighbor",
  packages=setuptools.find_packages(),
  python_requires=">=3.4",  # '>=3.4',  # 3.4.6
    install_requires=REQUIRED_PACKAGES,
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  'Intended Audience :: Developers',
 'Intended Audience :: Education',
 'Intended Audience :: Science/Research',
  'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
  ],
  keywords=['embedding', 'information retrieval',
              'deep learning', 'torch', 'tensor', 'pytorch','nearest neighbor']
)
