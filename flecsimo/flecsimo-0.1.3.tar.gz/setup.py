"""A setuptools based setup module.

See:
    https://packaging.python.org/guides/distributing-packages-using-setuptools/
    https://github.com/pypa/sampleproject
"""
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here/'README.md').read_text(encoding='utf-8')

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    # Name of the project.
    name='flecsimo',
    
    # Project version - should comply with PEP 440:
    # https://www.python.org/dev/peps/pep-0440/
    version='0.1.3',
    
    # one-line description or tagline of what the project does.
    description='A research/educational simulation model of a IIoT cellular production site.',
    
    # This is an optional longer description of your project that represents
    # the body of text which users will see when they visit PyPI.
    long_description=long_description,
    
    # Denotes that our long_description is in Markdown.
    long_description_content_type='text/markdown',
    
    # link to project's main homepage.
    url='https://gitlab.com/flecsimodev/flecsimo',
    
    author='Ralf Banning, Bernhard Lehner',
    author_email='banning@fb3.fra-uas.de',
    
    maintainer='Ralf Banning',
    maintainer_email='banning@fb3.fra-uas.de',
    
       
    # License qualitifer
    license='GPLv3+',
    
    
    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
    
        # Indicate who your project is intended for
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
    
        'Topic :: Education',
        'Topic :: Scientific/Engineering',    
        
        #License
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    
        # Supported Python versions
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    
        # Recomended operation systems
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows :: Windows 10',
    ],
    
    # This field adds keywords for the project which will appear on the
    # project page.
    keywords='cellular manufacturing, simulation, IIoT',

    # Add commandline scripts.
    scripts=['src/flecsimo/app/area_agent.py', 
             'src/flecsimo/app/area_control.py',
             'src/flecsimo/app/cell_agent.py',
             'src/flecsimo/app/site_agent.py',
             'src/flecsimo/app/site_control.py',
             'src/flecsimo/app/station_control.py'],

    # When your source code is in a subdirectory under the project root, e.g.
    # `src/`, it is necessary to specify the `package_dir` argument.
    package_dir={'': 'src'},
    
    # Include databases, config files and testdata which or non-py-sources.
    package_data={'': ['conf/*.json', 'db/*.db']},
    
    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    packages=find_packages(where='src', exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    
    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    #
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/en/latest/requirements.html    
    install_requires=[
        'paho-mqtt>=1.5.0',
        'transitions>=0.8.1',
        'memory-profiler>=0.57.0',
        'pyreadline>=2.1'
    ],
    
    # Specify which Python versions you support. In contrast to the
    # 'Programming Language' classifiers above, 'pip install' will check this
    # and refuse to install the project if the version does not match. See
    # https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires    
    python_requires='>=3.6, <4',
    
    # Additional URLs that are relevant to your project as a dict.
    # The key is  what's used to render the link text on PyPI.
    project_urls={
        'Documentation': 'https://confluence.frankfurt-university.de/display/FFP',
        'Source': 'https://gitlab.com/flecsimodev/flecsimo',
        'Tracker': 'https://gitlab.com/flecsimodev/flecsimo/-/issues',
    },
)