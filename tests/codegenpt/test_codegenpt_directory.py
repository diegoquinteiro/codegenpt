from codegenpt.codegenpt_directory import CodeGenPTDirectory
import pytest

@pytest.fixture
def test_directory():
    return CodeGenPTDirectory('tests/codegenpt/test_dir.dir.codegenpt')

def test_codegenpt_directory(test_directory: CodeGenPTDirectory):
    assert test_directory.fullPath == 'tests/codegenpt/test_dir'

    
def test_codegenpt_directory_context(test_directory: CodeGenPTDirectory):
    assert test_directory.context == {
        'directory_name': 'test_dir',
        'path': ['tests', 'codegenpt'],
    }