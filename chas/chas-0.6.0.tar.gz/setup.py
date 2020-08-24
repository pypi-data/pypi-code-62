import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chas",
    version="0.6.0",
    author="Lukas Cerny",
    author_email="lukas.cerny@exponea.com",
    description="Framework for creating and running cron jobs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["chas"],
    include_package_data=True,
    entry_points={
        "console_scripts": ["chas=chas.command_line:main"],
    },
    install_requires=["flask==1.1.2", "prometheus-flask-exporter==0.15.4", "prometheus_client==0.8.0",
                      "croniter==0.3.34"],
    url="https://github.com/lukasotocerny/chas",
    classifiers=[
        "Programming Language :: Python :: 3.6",
    ]
)
