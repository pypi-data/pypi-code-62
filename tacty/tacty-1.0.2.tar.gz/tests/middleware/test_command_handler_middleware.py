import unittest
from unittest.mock import Mock, patch

from tacty.handler import Handler
from tacty.middleware import CommandHandlerMiddleware


class TestCommand:
    pass


class TestHandler(Handler):
    def handle(self, command: TestCommand) -> None:
        pass


class TestCommandHandlerMiddleware(unittest.TestCase):
    @patch('tacty.resolver.InMemoryResolver')
    def test_assert_true(self, mock_resolver):
        # Arrange
        test_command = TestCommand()
        mock_test_handler = Mock()
        mock_test_handler.handle = Mock()
        mock_resolver.resolve = Mock()
        mock_resolver.resolve.return_value = mock_test_handler

        # Act
        middleware = CommandHandlerMiddleware(mock_resolver)
        middleware.execute(test_command, lambda *args: None)

        # Assert
        mock_resolver.resolve.assert_called_with(type(test_command))
        mock_test_handler.handle.assert_called_once_with(test_command)
