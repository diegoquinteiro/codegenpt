import glob
import os
from codegenpt.codegenpt_directory import CodeGenPTDirectory
from codegenpt.codegenpt_file import CodeGenPTFile;


# Find all codegenpt files in the given root directory
def find_codegenpt_files(path='', recursive=True):
    return list(map(
        lambda filename: CodeGenPTFile(filename),
        filter(
            lambda filename: not filename.endswith('.dir.codegenpt'),
            glob.glob(os.path.join(path, '**/*.codegenpt' if recursive else '*.codegenpt'), recursive=recursive)
        )
    ))

# Find all codegenpt directories in the given root directory
def find_codegenpt_directories(path='', recursive=True):
    return list(map(
        lambda dirname: CodeGenPTDirectory(dirname),
        glob.glob(os.path.join(path, '**/*.dir.codegenpt' if recursive else '*.dir.codegenpt'), recursive=recursive)
    ))