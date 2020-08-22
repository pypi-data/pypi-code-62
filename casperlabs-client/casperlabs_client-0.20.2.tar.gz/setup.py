#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import re
import errno
import urllib.request
import shutil
from glob import glob
from pathlib import Path
from shutil import copyfile
from typing import Union

from setuptools import setup, find_packages
from os import path
from os.path import basename, dirname, join

from setuptools.command.develop import develop as DevelopCommand
from setuptools.command.install import install as InstallCommand
from distutils.spawn import find_executable

THIS_DIRECTORY = Path(os.path.dirname(os.path.realpath(__file__)))

# Directory with Scala client's bundled contracts

CASPERLABS_DIR = THIS_DIRECTORY.parent / "CasperLabs"
PROTOBUF_DIR = THIS_DIRECTORY / "protobuf"
PROTO_DIR = THIS_DIRECTORY / "casperlabs_client" / "proto"
PACKAGE_DIR = THIS_DIRECTORY / "casperlabs_client"
VERSION_FILE = PACKAGE_DIR / "VERSION"
NAME = "casperlabs_client"


def read_version() -> str:
    with open(VERSION_FILE, "r") as f:
        return f.read().strip()


def proto_compiler_check():
    proto_c = find_executable("protoc")
    if proto_c is None:
        sys.stderr.write(
            "protoc is not installed. "
            "Please install Protocol Buffers binary package for your Operating System.\n"
        )
        sys.exit(-1)


def python_compiler_check():
    if sys.version < "3.7":
        sys.stderr.write(f"{NAME} is only supported on Python versions 3.7+.\n")
        sys.exit(-1)


def make_dirs(dir_path: Union[Path, str]):
    try:
        os.makedirs(dir_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def download(url, directory):
    make_dirs(directory)
    urllib.request.urlretrieve(url, join(directory, basename(url)))


def replace_in_place(pairs, file_name):
    import in_place

    with in_place.InPlace(file_name) as f:
        for line in f:
            for r, s in pairs:
                line = re.sub(r, s, line)
            f.write(line)


def modify_files(description, pairs, files):
    print(description)
    for file_name in files:
        print(f"   {file_name}")
        replace_in_place(pairs, file_name)


def run_protoc(file_names, proto_dir=PROTO_DIR):
    import grpc_tools
    from grpc_tools import protoc

    print("Run protoc...")
    google_proto = join(dirname(grpc_tools.__file__), "_proto")
    for file_name in file_names:
        print(f"   {file_name}")
        protoc.main(
            (
                "",
                f"-I{proto_dir}",
                "-I" + google_proto,
                f"--python_out={PACKAGE_DIR}",
                f"--python_grpc_out={PACKAGE_DIR}",
                f"--grpc_python_out={PACKAGE_DIR}",
                file_name,
            )
        )
    clean_up_source_files()


def collect_proto_files():
    print("Collect files...")

    for file_name in Path(PROTOBUF_DIR).glob("**/*.proto"):
        copyfile(file_name, PROTO_DIR / basename(file_name))

    print("Finished collecting files...")


def clean_up_source_files():
    try:
        shutil.rmtree(PROTO_DIR)
    except FileNotFoundError:
        pass


def clean_up_generated_files():
    for file_name in glob(f"{PACKAGE_DIR}/*pb2*py"):
        os.remove(file_name)
    for file_name in glob(f"{PACKAGE_DIR}/*grpc.py"):
        os.remove(file_name)


def run_codegen():
    python_compiler_check()
    proto_compiler_check()
    clean_up_source_files()
    clean_up_generated_files()
    make_dirs(f"{PROTO_DIR}")
    collect_proto_files()
    modify_files(
        "Patch proto files' imports", [(r'".+/', '"')], glob(f"{PROTO_DIR}/*.proto")
    )
    run_protoc(glob(f"{PROTO_DIR}/*.proto"))
    modify_files(
        "Patch generated Python gRPC modules",
        [(r"(import .*_pb2)", r"from . \1")],
        glob(f"{PACKAGE_DIR}/*pb2*py"),
    )
    # modify_files(
    #     "Patch generated Python gRPC modules (for asyncio)",
    #     [(r"(import .*_pb2)", r"from . \1")],
    #     [fn for fn in glob(f"{PACKAGE_DIR}/*_grpc[.]py") if "_pb2_" not in fn],
    # )


def prepare_sdist():
    run_codegen()


if len(sys.argv) > 1 and sys.argv[1] == "sdist":
    prepare_sdist()


with open(path.join(THIS_DIRECTORY, "README.md"), encoding="utf-8") as fh:
    long_description = fh.read()


class CInstall(InstallCommand):
    def run(self):
        super().run()


class CDevelop(DevelopCommand):
    def run(self):
        run_codegen()
        super().run()


setup(
    name=NAME,
    version=read_version(),
    packages=find_packages(),
    setup_requires=[
        "protobuf==3.12.2",
        "grpcio-tools>=1.20",
        "in-place==0.4.0",
        "grpcio>=1.20",
    ],
    install_requires=[
        "protobuf==3.12.2",
        "grpcio>=1.20",
        "grpclib==0.3.1",
        "pyblake2==1.1.2",
        "cryptography==2.8",
        "ecdsa==0.15",
        "pycryptodome==3.9.4",
    ],
    cmdclass={"install": CInstall, "develop": CDevelop},
    description="Python Client for interacting with a CasperLabs Node",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # Hardcoding name for missing version file when package is renamed.
    package_data={"casperlabs_client": [str(VERSION_FILE)]},
    keywords="casperlabs blockchain ethereum smart-contracts",
    author="CasperLabs LLC",
    author_email="testing@casperlabs.io",
    license="CasperLabs Open Source License (COSL)",
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
    url="https://casperlabs.io/",
    project_urls={
        "Source": "https://github.com/CasperLabs/CasperLabs/tree/dev/integration-testing/client/CasperLabsClient",
        "Readme": "https://github.com/CasperLabs/CasperLabs/blob/dev/integration-testing/client/CasperLabsClient/README.md",
    },
    entry_points={
        "console_scripts": ["casperlabs_client = casperlabs_client.cli:main"]
    },
)
