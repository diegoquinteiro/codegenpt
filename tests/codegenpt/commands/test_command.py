from codegenpt.commands.command import Command

def test_command_equality():
    assert Command("hello", []) == Command("hello", [])
    assert Command("hello", ["world"]) == Command("hello", ["world"])
    assert not Command("hello", ["world"]) == Command("hello", [])

def test_command_name():
    assert Command("hello").name == "hello"
    assert Command("world").name == "world"

def test_command_arguments():
    assert Command("hello", ["world"]).arguments == ["world"]
    assert Command("world", ["hello"]).arguments == ["hello"]