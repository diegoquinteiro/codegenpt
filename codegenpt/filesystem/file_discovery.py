import glob
from codegenpt.codegenpt_file import CodeGenPTFile;


# Find all codegenpt files in the given root directory
def find_codegenpt_files(root_dir=None, recursive=True):
    return list(map(
        lambda filename: CodeGenPTFile(filename),
        glob.glob('**/*.codegenpt', recursive=recursive, root_dir=root_dir)
    ))
