try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import os.path
import re

VERSION_RE = re.compile(r"""__version__ = ['"]([-a-z0-9.]+)['"]""")
BASE_PATH = os.path.dirname(__file__)


with open(os.path.join(BASE_PATH, "gcp_taskqueue", "__init__.py")) as f:
    try:
        version = VERSION_RE.search(f.read()).group(1)
    except IndexError:
        raise RuntimeError("Unable to determine version.")


with open(os.path.join(BASE_PATH, "README.md")) as readme:
    long_description = readme.read()


setup(
    name="gcp-taskqueue",
    description="google cloud task queue",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    version=version,
    author="Yingbo Gu",
    author_email="tensiongyb@gmail.com",
    maintainer="Yingbo Gu",
    maintainer_email="tensiongyb@gmail.com",
    url="https://github.com/guyingbo/gcp-taskqueue",
    packages=["gcp_taskqueue"],
    python_requires=">=3.6",
    install_requires=["google-cloud-tasks", "google-auth"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "coverage", "pytest-cov"],
)
