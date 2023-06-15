from os import path
import os
import click
from demjson3 import encode
from codegenpt.codegenpt_instructions import CodeGenPTInstructions

class CodeGenPTDirectory(CodeGenPTInstructions):

    @property
    def suffix(self):
        return '.dir.codegenpt'
        
    @property
    def context(self):
        return {
            'directory_name': self.basename,
            'path': self.path,
        }

    def create(self, content):
        if not path.exists(self.fullPath):
            os.mkdir(self.fullPath)
        with open(path.join(self.fullPath, '.codegenpt.json'), 'w') as file:
            file.write(encode(content))
        if "children" in content:
            
            # Create the include statements for the parent directories
            dir = self
            parent_dir = ''
            parent_includes = ['@include .codegenpt.json']
            while dir.parent is not None:
                parent_dir = path.join('..', parent_dir)
                parent_includes.append(f'@include {parent_dir}.codegenpt.json')
                dir = dir.parent
            parent_includes = '\n'.join(parent_includes) + '\n'

            for children in content["children"]:
                includes = parent_includes
                if "dependencies" in children:
                    includes = includes + '\n'.join([f"@include {dependency}" for dependency in children["dependencies"]]) + '\n'
                if "filename" in children:
                    with open(path.join(self.fullPath, children["filename"] + ".codegenpt"), 'w+') as file:
                        file.write(includes + children["prompt"])

                elif "dirname" in children:
                    with open(path.join(self.fullPath, children["dirname"] + ".dir.codegenpt"), 'w+') as file:
                        file.write(includes + children["prompt"])
                        if "children" in children:
                            CodeGenPTDirectory(self.fullPath + os.sep + children["dirname"], parent=self).create(children)