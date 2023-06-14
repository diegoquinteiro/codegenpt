from os import path
import os
from codegenpt.codegenpt_instructions import CodeGenPTInstructions

class CodeGenPTDirectory(CodeGenPTInstructions):
    
    @property
    def basename(self):
        return path.basename(self.fullPath)
        
    @property
    def context(self):
        return {
            'directory_name': self.basename,
            'path': self.path,
        }

    def write(self, content):
        os.mkdir(self.fullPath);
        with open(self.filename, "w+") as file:
            file.write(content)