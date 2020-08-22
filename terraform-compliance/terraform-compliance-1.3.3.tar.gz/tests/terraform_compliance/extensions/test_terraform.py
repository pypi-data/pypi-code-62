from unittest import TestCase
from terraform_compliance.extensions.terraform import TerraformParser, seek_key_in_dict
from tests.mocks import MockedData
from mock import patch
from ddt import ddt, data
from copy import deepcopy


@ddt
class TestTerraformParser(TestCase):


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_version_check_success(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['format_version'] = obj.supported_format_versions[0]
        obj.raw['terraform_version'] = obj.supported_terraform_versions[0]
        self.assertTrue(obj._version_check())


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_version_check_failure_unsupported_format_version(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['format_version'] = 'some_unsupported_format_version'
        obj.raw['terraform_version'] = obj.supported_terraform_versions[0]
        with self.assertRaises(SystemExit):
            obj._version_check()


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_version_check_failure_unsupported_terraform_version(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['format_version'] = obj.supported_format_versions[0]
        obj.raw['terraform_version'] = 'some_unsupported_terraform_version'
        with self.assertRaises(SystemExit):
            obj._version_check()


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_identify_data_file_success(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['values'] = True
        obj._identify_data_file()
        self.assertEqual(obj.file_type, 'state')


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_identify_data_file_failure(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj._identify_data_file()
        self.assertEqual(obj.file_type, 'plan')


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_variables(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['variables'] = True
        obj._parse_variables()
        self.assertEqual(obj.variables, True)


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_resources_resources_exists_in_the_plan_data(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['planned_values'] = {
            'root_module': {
                'resources': [
                    {
                        'address': 'data.something'
                    }
                ]
            }
        }
        obj._parse_resources()
        self.assertEqual(obj.data['data.something'], {'address': 'data.something'})


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_resources_resources_exists_in_the_plan_resource(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['planned_values'] = {
            'root_module': {
                'resources': [
                    {
                        'address': 'something'
                    }
                ]
            }
        }
        obj._parse_resources()
        self.assertEqual(obj.resources['something'], {'address': 'something'})


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_resources_resources_exists_in_the_state_data(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['values'] = {
            'root_module': {
                'resources': [
                    {
                        'address': 'data.something'
                    }
                ]
            }
        }
        obj._parse_resources()
        self.assertEqual(obj.data['data.something'], {'address': 'data.something'})


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_resources_resources_exists_in_the_state_resource(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['values'] = {
            'root_module': {
                'resources': [
                    {
                        'address': 'something'
                    }
                ]
            }
        }
        obj._parse_resources()
        self.assertEqual(obj.resources['something'], {'address': 'something'})


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_resources_child_resources_exists_in_the_state_data(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['values'] = {
            'root_module': {
                'child_modules': {
                    'resources': [
                        {
                            'address': 'data.something'
                        }
                    ]
                }
            }
        }
        obj._parse_resources()
        self.assertEqual(obj.data['data.something'], {'address': 'data.something'})


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_resources_child_resources_exists_in_the_state_resource(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['values'] = {
            'root_module': {
                'child_modules': {
                    'resources': [
                        {
                            'address': 'something'
                        }
                    ]
                }
            }
        }
        obj._parse_resources()
        self.assertEqual(obj.resources['something'], {'address': 'something'})

    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_resources_resources_exists_in_the_resource_changes_data(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['resource_changes'] = [
            {
                'mode': 'data',
                'address': 'data.something',
                'change': {
                    'actions': ['update'],
                    'before': {
                        'key': 'foo'
                    },
                    'after': {
                        'key': 'bar'
                    }
                }
            }
        ]
        obj._parse_resources()
        self.assertEqual(obj.data['data.something'], {'address': 'data.something', 'mode': 'data', 'values': {'key': 'bar'}})

    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_resources_resources_exists_in_the_resource_changes_resource(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['resource_changes'] = [
            {
                'address': 'something',
                'change': {
                    'actions': ['update'],
                    'before': {
                        'key': 'foo'
                    },
                    'after': {
                        'key': 'bar'
                    }
                }
            }
        ]
        obj._parse_resources()
        self.assertEqual(obj.resources['something'], {'address': 'something', 'values': {'key': 'bar'}})

    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_resources_resources_exists_in_the_resource_changes_deleted(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['resource_changes'] = [
            {
                'address': 'something',
                'change': {
                    'actions': ['delete'],
                    'before': {
                        'key': 'foo'
                    },
                    'after': {
                        'key': 'bar'
                    }
                }
            }
        ]
        obj._parse_resources()
        self.assertEqual(obj.resources, {})

    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_configurations_resources(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['configuration'] = {
            'root_module': {
                'resources': [
                    {
                        'address': 'something'
                    }
                ]
            }
        }
        obj._parse_configurations()
        self.assertEqual(obj.configuration['resources']['something'], {'address': 'something'})


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_configurations_variables(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['configuration'] = {
            'root_module': {
                'variables': [
                    {
                        'variable_key': 'variable_value'
                    }
                ]
            }
        }
        obj._parse_configurations()
        self.assertEqual(obj.configuration['variables'], [{'variable_key': 'variable_value'}])


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_configurations_providers(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['configuration'] = {
            'provider_config': {
                'some_provider': 'some_provider_data'
            }
        }
        obj._parse_configurations()
        self.assertEqual(obj.configuration['providers'], {'some_provider': 'some_provider_data'})

    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_configurations_module_resources(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['configuration'] = {
            'root_module': {
                'module_calls': {
                    'a_module':{
                        'module': {
                            'resources': [
                                {
                                    'address': 'something'
                                }
                            ]
                        }
                    }
                }
            }
        }
        obj._parse_configurations()
        self.assertEqual(obj.configuration['resources']['something'], {'address': 'something'})

    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_configurations_ignore_nested_resources(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['configuration'] = {
            'root_module': {
                'module_calls': {
                    'a_module':{
                        'expressions': {
                            'cluster_role_rules': {
                                'constant_values': [
                                    {
                                        "resources": [
                                            "namespaces",
                                            "pods"
                                        ]
                                    }
                                ]
                            }
                        }
                    }
                },
                'resources': [
                    {
                        'address': 'something'
                    }
                ]
            }
        }
        obj._parse_configurations()
        self.assertEqual(obj.configuration['resources']['something'], {'address': 'something'})

    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_mount_resources_with_ref_type(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        target = 'target_ref'
        source = 'source_ref'
        ref_type = 'some_key'
        obj.resources = {
            target: {
                'values': {
                    'some_key': ['a']
                }
            },
            source: {
                'values': {
                    'some_key': 'some_value'
                }
            }
        }
        obj.resources_raw = deepcopy(obj.resources)
        obj._mount_resources([source], {'some_key': [target]}, ref_type)
        self.assertEqual(['a', {'some_key': 'some_value', 'terraform-compliance.mounted': True}], obj.resources[target]['values'][ref_type])

    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_mount_resources_without_ref_type(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        target = 'target_ref'
        source = 'source_ref'
        ref_type = 'some_ref'
        obj.resources = {
            target: {
                'values': {}
            },
            source: {
                'values': {
                    'some_key': 'some_value'
                }
            }
        }
        obj.resources_raw = deepcopy(obj.resources)
        obj._mount_resources([source], {'some_key': [target]}, ref_type)
        self.assertEqual([{'some_key': 'some_value', 'terraform-compliance.mounted': True}], obj.resources[target]['values'][ref_type])

    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_mount_resources_failure_if_source_resource_does_not_have_values(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        target = 'target_ref'
        source = 'source_ref'
        ref_type = 'some_ref'
        obj.resources = {
            target: {
                'values': {}
            },
            source: {
            }
        }
        obj.resources_raw = deepcopy(obj.resources)
        obj._mount_resources([source], [target], ref_type)
        self.assertEqual({}, obj.resources[target]['values'])


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_find_resource_from_name_resource_name_in_resources(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.resources = {'something': True}
        self.assertEqual(obj._find_resource_from_name('something'), ['something'])


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_find_resource_from_name_resource_name_in_child_resources(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.resources = {
            'a': {
                'type': 'resource_type',
                'name': 'resource_id'
            }
        }
        self.assertEqual(obj._find_resource_from_name('resource_type.resource_id'), ['a'])

    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_find_resource_from_name_resource_name_in_module_outputs_expression_references(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['configuration'] = {
            "root_module": {
            "module_calls": {
                "module_name": {
                    "source": "../../module-test",
                    "module": {
                        "outputs": {
                            "my_expression": {
                                "expression": {
                                    "references": [
                                        "var.example"
                                    ]
                                }
                            }
                        }
                    }
                }
            }
            }
        }
        self.assertEqual(obj._find_resource_from_name('module.module_name.my_expression'), ['module.module_name.var.example'])

    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_find_resource_from_name_resource_name_in_module_outputs_expression(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['configuration'] = {
            "root_module": {
            "module_calls": {
                "module_name": {
                    "source": "../../module-test",
                    "module": {
                        "outputs": {
                            "my_expression": {
                                "expression": {
                                    "constant_value": [
                                        "10.123.0.0/16"
                                    ]
                                },
                                "description": "List of cidr(s)"
                            }
                        }
                    }
                }
            }
            }
        }
        self.assertEqual(obj._find_resource_from_name('module.module_name.my_expression'), [])

    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_distribute_providers(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.resources = {
            'provider_resource_id': {
                'type': 'resource_type',
                'name': 'resource_id'
            },
            'other-provider_other_resource_id': {
                'type': 'other-provider_other_resource_type',
                'name': 'resource_id'
            }
        }
        obj._distribute_providers()

        print(obj.providers)
        self.assertTrue('provider' in obj.providers)
        self.assertTrue('other-provider' in obj.providers)

    @patch.object(TerraformParser, '_read_file', return_value={})
    @patch.object(TerraformParser, '_version_check', return_value=None)
    @patch.object(TerraformParser, '_identify_data_file', return_value=None)
    @patch.object(TerraformParser, '_parse_resources', return_value=None)
    @patch.object(TerraformParser, '_parse_configurations', return_value=None)
    @patch.object(TerraformParser, '_mount_references', return_value=None)
    @patch.object(TerraformParser, '_distribute_providers', return_value=None)
    def test_parse_plan(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['variables'] = True
        obj.parse()

        self.assertEqual(obj.variables, True)

    @patch.object(TerraformParser, '_read_file', return_value={})
    @patch.object(TerraformParser, '_version_check', return_value=None)
    @patch.object(TerraformParser, '_identify_data_file', return_value=None)
    @patch.object(TerraformParser, '_parse_resources', return_value=None)
    @patch.object(TerraformParser, '_parse_configurations', return_value=None)
    @patch.object(TerraformParser, '_mount_references', return_value=None)
    @patch.object(TerraformParser, '_distribute_providers', return_value=None)
    def test_parse_state(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['variables'] = True
        obj.file_type = 'state'
        obj.parse()

        self.assertEqual(obj.variables, None)


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_find_resources_by_type_success(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.resources = {
            'provider_resource_id': {
                'type': 'resource_type',
                'name': 'resource_id',
                'mode': 'managed'
            },
            'other-provider_other_resource_id': {
                'type': 'other-provider_other_resource_type',
                'name': 'resource_id',
                'mode': 'managed'
            }
        }

        self.assertEqual(obj.find_resources_by_type('resource_type'),
                         [{
                            'type': 'resource_type',
                            'name': 'resource_id',
                            'mode': 'managed'
                          }])

    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_find_resources_by_type_failure(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.resources = {
            'provider_resource_id': {
                'type': 'resource_type',
                'name': 'resource_id',
                'mode': 'managed'
            },
            'other-provider_other_resource_id': {
                'type': 'other-provider_other_resource_type',
                'name': 'resource_id',
                'mode': 'managed'
            }
        }

        self.assertEqual(obj.find_resources_by_type('invalid_resource'),
                         [])

    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_expand_resource_tags_success(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.resources = {
            'provider_resource_id': {
                'type': 'resource_type',
                'name': 'resource_id',
                'mode': 'managed',
                'values': {
                    'tags': [
                        {
                        'key': 'somekey',
                        'value': 'somevalue',
                        'someotherkey': True
                        }
                    ]
                }
            },
            'other-provider_other_resource_id': {
                'type': 'other-provider_other_resource_type',
                'name': 'resource_id',
                'mode': 'managed',
                'values': {}
            }
        }
        obj._expand_resource_tags(obj.resources['provider_resource_id'])
        obj._expand_resource_tags(obj.resources['other-provider_other_resource_id'])
        self.assertTrue('somekey' in obj.resources['provider_resource_id']['values']['tags'][0])
        self.assertEqual(obj.resources['provider_resource_id']['values']['tags'][0]['somekey'], 'somevalue')
        self.assertEqual(obj.resources['provider_resource_id']['values']['tags'][0]['key'], 'somekey')
        self.assertEqual(obj.resources['provider_resource_id']['values']['tags'][0]['someotherkey'], True)
        self.assertTrue('tags' not in obj.resources['other-provider_other_resource_id']['values'])

    @patch.object(TerraformParser, '_read_file', return_value={})
    @data([], {}, '', 123, [dict(a='b')])
    def test_expand_resource_tags_failures(self, value, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.resources = {
            'provider_resource_id': {
                'type': 'resource_type',
                'name': 'resource_id',
                'mode': 'managed',
                'values': {
                    'tags': [
                        value
                    ]
                }
            },
            'other-provider_other_resource_id': {
                'type': 'other-provider_other_resource_type',
                'name': 'resource_id',
                'mode': 'managed',
                'values': {}
            }
        }
        obj._expand_resource_tags(obj.resources['provider_resource_id'])
        obj._expand_resource_tags(obj.resources['other-provider_other_resource_id'])
        self.assertTrue('tags' not in obj.resources['other-provider_other_resource_id']['values'])
        self.assertEqual(value, obj.resources['provider_resource_id']['values']['tags'][0])

