import json
import sys
from lambda_common.aws_message_helper import get_message_body_from_record


class TestAwsMessageHelper:
    def test_get_message_body_from_record(self):
        # Arrange
        expected_body = "{\"field1\": \"value1\", \"field2\":\"value2\"}"

        # Act
        current_body = get_message_body_from_record(
            record={
                "body": expected_body
            }
        )

        # Assert
        assert current_body == json.loads(expected_body)

    def test_get_message_body_from_record_is_invalid_body(self):
        # Arrange
        expected_body = "invalid body"

        # Act
        current_body = get_message_body_from_record(
            record={
                "body": expected_body
            }
        )

        # Assert
        assert current_body == {}
