import os
from ..commands.command import Command

def test_equality():
    command1 = Command("create")
    command2 = Command("create")
    assert command1 == command2

def test_create_command():
    command = Command("create", ["file.txt"])
    assert command.name == "create"
    assert command.arguments == ["file.txt"]

def test_edit_command():
    command = Command("edit", ["file.txt"])
    assert command.name == "edit"
    assert command.arguments == ["file.txt"]

def test_remove_command():
    command = Command("remove", ["file.txt"])
    assert command.name == "remove"
    assert command.arguments == ["file.txt"]

def test_execute_command():
    command = Command("execute", ["script.sh"])
    assert command.name == "execute"
    assert command.arguments == ["script.sh"]