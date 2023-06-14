from codegenpt.commands.commands import Commands
from codegenpt.commands.command import Command
from codegenpt.codegenpt_file import CodeGenPTFile

def test_run_registered_command():

    file = CodeGenPTFile('test.txt')

    Commands.registerCommandRunner('test', lambda cmd, f, msgs: ['test'])

    messages = Commands.run(Command('test'), file, [])

    assert messages == ['test']