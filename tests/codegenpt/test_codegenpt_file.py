from textwrap import dedent
import pytest
from codegenpt.codegenpt_file import CodeGenPTFile
from codegenpt.commands.command import Command


@pytest.fixture
def test_file():
    return CodeGenPTFile('tests/test_files/test.py.codegenpt')


def test_codegenpt_file(test_file: CodeGenPTFile):
    assert test_file.filename == 'tests/test_files/test.py'


def test_codegenpt_file_extension(test_file: CodeGenPTFile):
    assert test_file.extension == 'py'


def test_codegenpt_file_prompt(test_file: CodeGenPTFile):
    assert test_file.prompt == dedent('''\
            Read the @jokes.txt file and generate a program that outputs the second joke.''')


def test_codegenpt_file_path(test_file: CodeGenPTFile):
    assert test_file.path == ['tests', 'test_files']


def test_codegenpt_file_basename(test_file: CodeGenPTFile):
    assert test_file.basename == 'test.py'


def test_codegenpt_file_context(test_file: CodeGenPTFile):
    assert test_file.context == {
        'basename': 'test.py',
        'extension': 'py',
        'path': ['tests', 'test_files'],
    }


def test_codegenpt_file_commands(test_file: CodeGenPTFile):
    assert test_file.commands == [
        Command(name='include', arguments=['jokes.txt']),
    ]
