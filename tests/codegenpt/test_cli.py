import os
from click.testing import CliRunner
import pytest
from codegenpt.cli import codegenpt, cli

@pytest.fixture(autouse=True)
def setup():
    if (os.path.exists('tests/test_files/test.py')):
        os.remove('tests/test_files/test.py')
    if (os.path.exists('tests/test_files/test.txt')):
        os.remove('tests/test_files/test.txt')
    yield
    
def test_codegenpt():
    codegenpt()
    assert os.path.exists('tests/test_files/test.py')
    assert os.path.exists('tests/test_files/test.txt')

def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code == 0