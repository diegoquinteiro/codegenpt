import os
import pytest
from unittest.mock import patch

from codegenpt.commands.include import include, Command

MOCKED_FILES = {
    "file1.txt": "I'm a file!",
    "file2.txt": "I'm a second file!"
}


def mock_file_content_generator(filename):
    with open(filename, "r") as file:
        return file.read()


class TestInclude:

    @pytest.mark.parametrize("command_arguments, expected_responses", [
        (["file1.txt"], ["OK"]),
        (["/file1.txt", "/file2.txt"], ["OK", "OK"]),
    ])
    @patch("builtins.open")
    @patch.object(os.path, "isfile")
    def test_include(
            self,
            mocked_isfile,
            mocked_file_open,
            command_arguments,
            expected_responses
    ):
        mocked_isfile.return_value = True
        mocked_file_open.side_effect = [
            mock_file_content_generator(f"{filename}")
            for filename in command_arguments
        ]

        # Instantiate Command object
        command = Command("include", command_arguments)

        # Instantiate CodeGenPTFile object
        file = CodeGenPTFile('__filename__')

        # Mock chatbot action
        messages = [{"role": "user", "content": str(command)}]
        returned_messages = include(command, file, messages)

        # Tests
        assert len(expected_responses) == len(returned_messages) - 1
        for i, message in enumerate(returned_messages):
            if i == 0:
                assert message == messages[i]
            else:
                assert message["content"] == expected_responses[i - 1]
                assert message["role"] == "assistant"