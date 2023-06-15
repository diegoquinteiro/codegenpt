import os
import pytest
from unittest.mock import MagicMock, patch
from click.testing import CliRunner
from codegenpt import cli
import codegenpt.llm.llm

@pytest.fixture(autouse=True)
def setup(monkeypatch):
    # Mock LLM
    monkeypatch.setattr('codegenpt.generators.file_generator.askLLM', lambda messages: f'Respose for {messages}')
    monkeypatch.setattr('codegenpt.generators.directory_generator.askLLM', lambda messages: f'Respose for {messages}')

    if (os.path.exists('tests/test_files/test.py')):
        os.remove('tests/test_files/test.py')
    if (os.path.exists('tests/test_files/test.txt')):
        os.remove('tests/test_files/test.txt')
    
    yield
    
    # Cleanup
    if (os.path.exists('tests/test_files/test.py')):
        os.remove('tests/test_files/test.py')
    if (os.path.exists('tests/test_files/test.txt')):
        os.remove('tests/test_files/test.txt')

def test_codegenpt(monkeypatch):
    cli.codegenpt(path='tests/test_files', force=False)
    assert os.path.exists('tests/test_files/test.py')
    assert os.path.exists('tests/test_files/test.txt')

def test_cli(monkeypatch):
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['-R', 'tests/test_files'])
    assert result.exit_code == 0