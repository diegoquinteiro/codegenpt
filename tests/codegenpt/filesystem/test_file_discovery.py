from codegenpt.filesystem.file_discovery import find_codegenpt_files


def test_find_codegenpt_files():
    files = find_codegenpt_files()
    assert len(files) > 0
    assert 'test.py' in map(lambda file: file.filename, files)
    assert 'test.txt' in map(lambda file: file.filename, files)

def test_find_codegenpt_files_non_recursively():
    files = find_codegenpt_files(recursive=False)
    assert len(files) == 0

def test_find_codegenpt_files_with_root_dir():
    files = find_codegenpt_files(path='tests/test_files')
    assert len(files) > 0
    assert ['tests', 'test_files'] in map(lambda file: file.path, files)