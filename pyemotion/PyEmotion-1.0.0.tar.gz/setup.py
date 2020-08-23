import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="PyEmotion",
  version="1.0.0",
  author="Karthick Nagarajan",
  author_email="karthick965938@gmail.com",
  description="A PyTorch library for detecting facial emotions",
  long_description=long_description,
  long_description_content_type="text/markdown",
  keywords='image data datascience emotion PyEmotion expression ML ml machinelearning AI ai',
  license='MIT',
  # url="https://github.com/karthick965938/PyEmotion",
  packages=setuptools.find_packages(),
  include_package_data=True,
  package_data={
    "PyEmotion": ["model/main_model.pkl"],
  },
  install_requires=[
    'opencv-python',
    'Pillow',
    'art',
    'termcolor',
    'progress',
    'pytest',
    'facenet_pytorch',
    'numpy'
  ],
  dependency_links = [
    'https://pypi.org/project/torch/1.5.1/'
  ],
  classifiers=[
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ]
)