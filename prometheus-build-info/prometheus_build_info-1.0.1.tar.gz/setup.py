from setuptools import setup, find_packages

KEYWORDS = ["metrics", "prometheus", "build"]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='prometheus_build_info',
    version='1.0.1',
    packages=find_packages(),
    include_package_data=True,
    url='',
    license='MIT',
    author='Niels Albers',
    author_email='nralbers@gmail.com',
    description='Utility project for recording build information and exposing it as a prometheus metric',
    install_requires=['click', 'prometheus_client'],
    entry_points='''
        [console_scripts]
        make-build-info=prometheus_build_info.builder:make_build_info
    ''',
    keywords=KEYWORDS,
    long_description=long_description,
    long_description_content_type="text/markdown; charset=UTF-8",
    python_requires='~=3.5',
    classifiers=[
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Monitoring",
        "Topic :: Software Development :: Build Tools",
        "Intended Audience :: Developers"
    ],
)
