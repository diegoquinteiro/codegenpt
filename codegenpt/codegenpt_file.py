from os import path
from codegenpt.codegenpt_instructions import CodeGenPTInstructions

from codegenpt.commands.command import Command

class CodeGenPTFile(CodeGenPTInstructions):

    @property
    def extension(self):
        return self.basename.split('.')[-1]
        
    @property
    def context(self):
        return {
            'filename': self.basename,
            'extension': self.extension,
            'path': self.path,
        }

    def write(self, content):
        with open(self.fullPath, "w+") as file:
            file.write(content)