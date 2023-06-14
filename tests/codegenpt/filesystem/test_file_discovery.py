from codegenpt.filesystem.file_discovery import find_codegenpt_directories, find_codegenpt_files


def test_find_codegenpt_files():
    files = find_codegenpt_files()
    assert len(files) > 0
    assert 'test.py' in map(lambda file: file.basename, files)
    assert 'test.txt' in map(lambda file: file.basename, files)

def test_find_codegenpt_directories():
    dirs = find_codegenpt_directories()
    assert len(dirs) > 0
    assert 'python_program' in map(lambda dir: dir.basename, dirs)

def test_find_codegenpt_files_non_recursively():
    files = find_codegenpt_files(recursive=False)
    assert len(files) == 0

def test_find_codegenpt_files_with_root_dir():
    files = find_codegenpt_files(path='tests/test_files')
    assert len(files) > 0
    assert ['tests', 'test_files'] in map(lambda file: file.path, files)