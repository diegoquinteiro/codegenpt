from os import path
from codegenpt.codegenpt_instructions import CodeGenPTInstructions

from codegenpt.commands.command import Command

class CodeGenPTFile(CodeGenPTInstructions):

    @property
    def extension(self):
        return self.filename.split('.')[-1]
    
    @property
    def filename(self):
        return path.basename(self.fullPath)
        
    @property
    def context(self):
        return {
            'filename': self.filename,
            'extension': self.extension,
            'path': self.path,
        }

    def write(self, content):
        with open(self.fullPath, "w+") as file:
            file.write(content)