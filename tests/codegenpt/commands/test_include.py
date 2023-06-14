from unittest.mock import MagicMock, call, mock_open, patch
from codegenpt.codegenpt_file import CodeGenPTFile
from codegenpt.commands.command import Command
from codegenpt.commands.include import include, command_message

def test_include(monkeypatch):
    m = mock_open(read_data="file opened")
    monkeypatch.setattr('builtins.open', m)

    messages = include(
        Command('@include', ['name.txt']),
        CodeGenPTFile('test.txt'),
        [{'role': 'system', 'content': 'system_message' }]
    )
    
    assert messages == [
        {'role': 'system', 'content': 'system_message' },
        {'role': 'user', 'content': command_message },
        {'role': 'assistant', 'content': 'OK'}, 
        {'role': 'user', 'content': '@include\n- File name: name.txt\nfile opened'},
        {'role': 'assistant', 'content': 'OK'}
    ]