import unittest
import time

from m2m_token.errors import ConfigError
from m2m_token.token import generate


class TokenTests(unittest.TestCase):

    def test_generate_raiseconfigerror_seed(self):
        test_values = [None, ""]
        for test_value in test_values:
            with self.assertRaises(ConfigError) as raised:
                generate(test_value, 1)
        exception: ConfigError = raised.exception
        self.assertEqual(exception.config_name, 'seed')

    def test_generate_raiseconfigerror_ttl(self):
        test_values = [None, -1]
        for test_value in test_values:
            with self.assertRaises(ConfigError) as raised:
                generate("test", test_value)
        exception: ConfigError = raised.exception
        self.assertEqual(exception.config_name, 'ttl')

    def test_generate_raiseconfigerror_sequence(self):
        test_values = [None, -1, ""]
        for test_value in test_values:
            with self.assertRaises(ConfigError) as raised:
                generate("test", 1, sequence=test_value)
        exception: ConfigError = raised.exception
        self.assertEqual(exception.config_name, 'sequence')

    def test_generate_raiseconfigerror_token_len(self):
        test_values = [None, -1, ""]
        for test_value in test_values:
            with self.assertRaises(ConfigError) as raised:
                generate("test", 1, token_len=test_value)
        exception: ConfigError = raised.exception
        self.assertEqual(exception.config_name, 'token_len')

    def test_generate_nominal(self):
        token = generate('seed', 3)
        self.assertIsNotNone(token)
        self.assertTrue(type(token) is str)
        self.assertEqual(6, len(token))
        token2 = generate('seed', 3)
        self.assertEqual(token, token2)

    def test_generate_nominaldifftoken(self):
        token1 = generate('seed', 3)
        self.assertIsNotNone(token1)
        self.assertTrue(type(token1) is str)
        token2 = generate('anotherSeed', 3)
        self.assertIsNotNone(token2)
        self.assertTrue(type(token2) is str)
        self.assertNotEqual(token1, token2)

    def test_generate_difftokentiming(self):
        token1 = generate('seed', 1)
        time.sleep(1)
        token2 = generate('seed', 1)
        self.assertNotEqual(token1, token2)
