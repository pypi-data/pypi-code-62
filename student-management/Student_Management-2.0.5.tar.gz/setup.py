from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="Student_Management",
    version="2.0.5",
    description="test",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/jesvinvijesh/Student_Management",
    author="Jesvin Vijesh S",
    author_email="nikhilksingh97@gmail.com",
    license="MIT",
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    packages=["students","students.migrations"],
    include_package_data=True,
)