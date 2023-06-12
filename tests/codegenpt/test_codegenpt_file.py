from textwrap import dedent
import pytest
from codegenpt.codegenpt_file import CodeGenPTFile

@pytest.fixture
def test_file():
    return CodeGenPTFile('tests/test_files/test.py.codegenpt')

def test_codegenpt_file(test_file: CodeGenPTFile):
    with test_file as file:
        assert file.filename == 'tests/test_files/test.py'

def test_codegenpt_file_extension(test_file: CodeGenPTFile):
    with test_file as file:
        assert file.extension == 'py'

def test_codegenpt_file_prompt(test_file: CodeGenPTFile):
    with test_file as file:
        assert file.prompt == dedent('''\
            Generate a hello world program.
            It should print a joke.''')
        
def test_codegenpt_file_path(test_file: CodeGenPTFile):
    with test_file as file:
        assert file.path == ['tests', 'test_files']

def test_codegenpt_file_basename(test_file: CodeGenPTFile):
    with test_file as file:
        assert file.basename == 'test.py'

def test_codegenpt_file_context(test_file: CodeGenPTFile):
    with test_file as file:
        assert file.context == {
            'basename': 'test.py',
            'extension': 'py',
            'path': ['tests', 'test_files'],
        }