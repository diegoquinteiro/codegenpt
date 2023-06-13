import pytest
from codegenpt.commands.command import Command

def test_command_init():
    cmd = Command("name", ["arg1", "arg2"])
    assert cmd.name == "name"
    assert cmd.arguments == ["arg1", "arg2"]

def test_command_eq():
    cmd1 = Command("name1", ["arg1", "arg2"])
    cmd2 = Command("name1", ["arg1", "arg2"])
    cmd3 = Command("name1", ["arg3", "arg4"])
    cmd4 = Command("name4", ["arg1", "arg2"])
    
    assert cmd1 == cmd2
    assert cmd1 != cmd3
    assert cmd1 != cmd4
    assert cmd4 != cmd3