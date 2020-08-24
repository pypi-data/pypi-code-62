import argparse
import json
import os
import unittest

import materials_commons.api as mcapi

import materials_commons.cli.tree_functions as treefuncs
from materials_commons.cli.file_functions import isfile, isdir
from materials_commons.cli.subcommands.dataset import DatasetSubcommand

from .cli_test_project import make_basic_project_1, test_project_directory, make_file, remove_if

def is_equal(A, B):
    if not type(A) is type(B):
        return False
    return A.__dict__ == B.__dict__

class TestMCDataset(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        project_name = "__clitest__dataset"
        project_path = os.path.join(test_project_directory(), project_name)
        self.basic_project_1 = make_basic_project_1(project_path)

        # initialize a Materials Commons Client
        mcurl = os.environ.get("MC_API_URL")
        email = os.environ.get("MC_API_EMAIL")
        password = os.environ.get("MC_API_PASSWORD")
        self.client = mcapi.Client.login(email, password, base_url=mcurl)

        # make sure test project does not already exist
        result = self.client.get_all_projects()
        for proj in result:
            if proj.name == project_name:
                self.client.delete_project(proj.id)

        # create a Materials Commons project
        self.proj = self.client.create_project(project_name)
        self.proj.local_path = project_path
        self.proj.remote = self.client
        self.assertEqual(self.proj.root_dir.name, "/")

    def tearDown(self):
        # clean up
        self.basic_project_1.clean_files()
        self.client.delete_project(self.proj.id)

    def test_parse_args(self):
        testargs = ['mc', 'dataset']
        dataset_subcommand = DatasetSubcommand()
        args = dataset_subcommand.parse_args(testargs)
        self.assertEqual(isinstance(args, argparse.Namespace), True)
