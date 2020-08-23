"""Tests that the agent module works correctly"""
from unittest import TestCase
from unittest.mock import Mock

import gym
import torch
import numpy as np
from pl_bolts.models.rl.common.agents import Agent, PolicyAgent, ValueAgent


class TestAgents(TestCase):

    def setUp(self) -> None:
        self.env = gym.make("CartPole-v0")
        self.state = self.env.reset()
        self.net = Mock()

    def test_base_agent(self):
        agent = Agent(self.net)
        action = agent(self.state, 'cuda:0')
        self.assertIsInstance(action, list)


class TestValueAgent(TestCase):

    def setUp(self) -> None:
        self.env = gym.make("CartPole-v0")
        self.net = Mock(return_value=torch.Tensor([[0.0, 100.0]]))
        self.state = [self.env.reset()]
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.value_agent = ValueAgent(self.net, self.env.action_space.n)

    def test_value_agent(self):

        action = self.value_agent(self.state, self.device)
        self.assertIsInstance(action, list)
        self.assertIsInstance(action[0], int)

    def test_value_agent_get_action(self):
        action = self.value_agent.get_action(self.state, self.device)
        self.assertIsInstance(action, np.ndarray)
        self.assertEqual(action[0], 1)

    def test_value_agent_random(self):
        action = self.value_agent.get_random_action(self.state)
        self.assertIsInstance(action[0], int)


class TestPolicyAgent(TestCase):

    def setUp(self) -> None:
        self.env = gym.make("CartPole-v0")
        self.net = Mock(return_value=torch.Tensor([[0.0, 100.0]]))
        self.states = [self.env.reset()]
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def test_policy_agent(self):
        policy_agent = PolicyAgent(self.net)
        action = policy_agent(self.states, self.device)
        self.assertIsInstance(action, list)
        self.assertEqual(action[0], 1)
