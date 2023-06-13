```python
import pytest
from codegenpt.codegenpt_file import CodeGenPTFile
from commands import Commands


def test_register_command_runner():
    command_name = 'test_command'
    def command_runner(command: Command, file: CodeGenPTFile, messages):
        return messages
    original_command_count = len(Commands.commandRunners)
    Commands.registerCommandRunner(command_name, command_runner)
    assert len(Commands.commandRunners) == original_command_count + 1

def test_run():
    file = CodeGenPTFile('')
    message = ['example_message']
    command = Command('include', '- File name: example_file')
    returned_message = Commands.run(command, file, message)
    assert message[0] == 'example_message'
    assert returned_message == message
```