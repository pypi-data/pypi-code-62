from setuptools import setup

import os

__version__ = '1.0.0'

gitlab_url = 'https://gitlab.com/florezjose'
package_name = 'menu_header_wagtail'
package_url = '{}/{}'.format(gitlab_url, package_name)
package_path = os.path.abspath(os.path.dirname(__file__))
long_description_file_path = os.path.join(package_path, 'README.md')
long_description_content_type = 'text/markdown'
long_description = ''
try:
    with open(long_description_file_path) as f:
        long_description = f.read()
except IOError:
    pass


setup(
    name=package_name,
    version=__version__,
    packages=['menu_header_wagtail'],
    include_package_data=True,
    description='Full navigation header, menus, sub menus, internal and external links and documents, '
                'simple integrated design.',
    long_description=long_description,
    long_description_content_type=long_description_content_type,
    author='Jose Flórez (@rojosefo)',
    author_email='florezjoserdolfo@gmail.com',
    url=package_url,
    download_url='{}/archive/{}.tar.gz'.format(package_url, __version__),
    keywords=['django', 'wagtail', 'fields', 'dynamic', 'theme', 'color',
              'checkbox', 'boolean', 'choices', 'chooser', 'admin', 'python'],
    requires=[
        "django(>=3.0)",
        "wagtail(>=2.8)"
    ],
    install_requires=[
        "Django>=3.0",
        "Pillow>=4.0.0,<8.0.0"
    ],
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Framework :: Wagtail',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Build Tools',
    ],
)
