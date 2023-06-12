from codegenpt.filesystem.file_discovery import find_codegenpt_files


def test_find_codegenpt_files():
    files = find_codegenpt_files()
    assert len(files) == 2
    assert files[0].basename == 'test.py'
    assert files[1].basename == 'test.txt'

def test_find_codegenpt_files_non_recursively():
    files = find_codegenpt_files(recursive=False)
    assert len(files) == 0

def test_find_codegenpt_files_with_root_dir():
    files = find_codegenpt_files(path='tests/test_files')
    assert len(files) == 2
    assert files[0].path == ['tests', 'test_files']
    assert files[1].path == ['tests', 'test_files']