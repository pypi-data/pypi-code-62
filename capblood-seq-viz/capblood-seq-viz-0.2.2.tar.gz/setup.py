from setuptools import setup

setup(
    name='capblood-seq-viz',
    version='0.2.2',
    description='Interactive visualization web app for capillary blood data',
    url='https://github.com/ThomsonLab/capblood-seq-viz',
    author='David Brown',
    author_email='dibidave@gmail.com',
    license='MIT',
    packages=[
        "capblood_seq_viz",
        "capblood_seq_viz.data",
        "capblood_seq_viz.config",
        "capblood_seq_viz.layouts",
        "capblood_seq_viz.assets",
        "capblood_seq_viz.common",
        "capblood_seq_viz.functions",
        "capblood_seq_viz.figures"
    ],
    package_data={
        "capblood_seq_viz.config": [
            "default.json"
        ],
        "capblood_seq_viz.assets": [
            "blood_logo.png",
            "favicon.ico"
        ]
    },
    entry_points={
        "console_scripts": [
            "capblood-seq-viz=capblood_seq_viz.launch:launch_server"
        ]
    },
    python_requires='~=3.6',
    include_package_data=True,
    install_requires=[
        "capblood-seq>=0.2.2",
        "gunicorn>=20.0.4,<21",
        "dash>=1.9.1",
        "dash-core-components>=1.8.1",
        "dash-html-components>=1.0.2",
        "dash-renderer>=1.2.4",
        "dash-bootstrap-components>=0.9.1",
        "dash-table>=4.6.1",
        "plotly",
        "flask",
        "importlib-resources>=1.4.0",
        "pandas",
        "numpy",
        "bioservices"
    ]

)
