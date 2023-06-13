import pytest
from unittest.mock import MagicMock
from codegenpt.codegenpt_file import CodeGenPTFile
from codegenpt.commands.commands import Commands

def test_run_command_expected_method_called():
    include_command = MagicMock()
    include_command.name = 'include'

    def include_mock(command, file, messages):
        return ['Import generated from include command!']

    Commands.registerCommandRunner('include', include_mock)
    result = Commands.run(include_command, CodeGenPTFile('test.txt'), [])
    assert len(result) > 0
    assert result[0] == 'Import generated from include command!'