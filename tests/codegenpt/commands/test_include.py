from unittest import mock

from codegenpt.commands.include import include, Command
from codegenpt.codegenpt_file import CodeGenPTFile

def test_include():
    file = CodeGenPTFile('test_include')
    command = Command(name="include", arguments=["file1.txt"])
    messages = [{}]

    with mock.patch('builtins.open', mock.mock_open(read_data='file content')):
        messages = include(command, file, messages)

    assert {
        "role": "user",
        "content": "@include\n- File name: file1.txt\nfile content"
    } in messages