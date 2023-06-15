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
            click.echo(f'📁 created directory: {self.fullPath}')
            os.mkdir(self.fullPath)
        with open(path.join(self.fullPath, '.codegenpt.json'), 'w') as file:
            click.echo(f'📄 created file: {self.fullPath}.codegenpt.json')
            file.write(encode(content))
        if "children" in content:
            click.echo(f'🗂️ creating files for: {self.fullPath}')
            
            # Create the include statements for the parent directories
            dir = self
            parent_dir = ''
            includes = ['@include .codegenpt.json']
            while dir.parent is not None:
                parent_dir = path.join('..', parent_dir)
                includes.append(f'@include {parent_dir}.codegenpt.json')
                dir = dir.parent
            includes = '\n'.join(includes) + '\n'

            for children in content["children"]:
                if "filename" in children:
                    with open(path.join(self.fullPath, children["filename"] + ".codegenpt"), 'w+') as file:
                        click.echo(f'📄 created file: {path.join(self.fullPath, children["filename"] + ".codegenpt")}')
                        file.write(includes + children["prompt"])

                elif "dirname" in children:
                    with open(path.join(self.fullPath, children["dirname"] + ".dir.codegenpt"), 'w+') as file:
                        click.echo(f'📄 created file: {path.join(self.fullPath, children["dirname"] + ".dir.codegenpt")}')
                        file.write(includes + children["prompt"])
                        if "children" in children:
                            CodeGenPTDirectory(self.fullPath + os.sep + children["dirname"], parent=self).create(children)