from lyncs_setuptools import setup, CMakeExtension

setup(
    "lyncs_clime",
    ext_modules=[CMakeExtension("lyncs_clime.clime", ".")],
    data_files=[("test", ["test/conf.unity"])],
    install_requires=["lyncs-cppyy",],
    keywords=["Lyncs", "c-lime", "Lattice QCD",],
    extras_require={"test": ["pytest", "pytest-cov",]},
    entry_points={"console_scripts": ["lyncs_lime_content = lyncs_clime:reader.main",]},
)
