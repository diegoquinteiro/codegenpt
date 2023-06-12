import glob
import os
from codegenpt.codegenpt_file import CodeGenPTFile;


# Find all codegenpt files in the given root directory
def find_codegenpt_files(path='', recursive=True):
    return list(map(
        lambda filename: CodeGenPTFile(filename),
        glob.glob(os.path.join(path, '**/*.codegenpt'), recursive=recursive)
    ))
