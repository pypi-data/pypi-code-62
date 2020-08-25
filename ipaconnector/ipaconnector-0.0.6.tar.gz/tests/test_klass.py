import os
import json
from unittest import TestCase
from ipaconnector.klass import User, AppUser


def get_sample(sample='./sample.json'):
    sample_path = os.path.join(os.path.dirname(__file__), sample)
    with open(sample_path) as _file:
        output = json.load(_file)
    return output


class TestUser(TestCase):
    def test_user(self):
        data = get_sample()['CREATIONS']['HumanUser'][0]
        ut = User(data)
        self.assertEqual(ut.login, 'jdoe')
        self.assertEqual(ut.full_name, 'John Doe')
        self.assertEqual(ut.email, 'jdoe@companyone.xyz')
        self.assertEqual(ut.homedir, '/data01/jdoe/')
        self.assertEqual(ut.gecos, 'FR/C//BYTEL/John Doe')

    def test_user_with_missing_info_should_create_with_none(self):
        data = \
            {"firstname": {"newValue": "John"
                           }, "keytab": {"newValue": "true"
                                         }, "company": {"newValue": "company one"
                                                        }, "team": {"newValue": "MOE"
                                                                    }, "login": {"newValue": "jdoe"
                                                                                 }, "primaryKey": {"login": "jdoe"}}
        ut = User(data)
        self.assertEqual(ut.login, 'jdoe')
        self.assertEqual(ut.full_name, 'John ')
        self.assertEqual(ut.email, None)
        self.assertEqual(ut.homedir, '/data01/jdoe/')
        self.assertEqual(ut.gecos, 'FR/C//BYTEL/John ')


class TestAppUser(TestCase):
    def test_user(self):
        data = get_sample("./delta_test_creations.json")['CREATIONS']['AppUser'][0]
        ut = AppUser(data)
        self.assertEqual('elaint_test1', ut.login)
        self.assertEqual('Application elaint_test1', ut.full_name)
        self.assertEqual('', ut.email)
        self.assertEqual('/data01/elaint_test1/', ut.homedir)
        self.assertEqual('FR/C//BYTEL/Test app user 1', ut.gecos)
