from os import path
import os
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
        os.mkdir(self.fullPath);
        with open(path.join(self.fullPath, '.codegenpt.json'), 'w') as file:
            file.write(encode(content))
        
        for children in content["children"]:
            if "filename" in children:
                with open(path.join(self.fullPath, children["filename"] + ".codegenpt"), 'w+') as file:
                    file.write('@include .codegenpt.json\n' + children["prompt"])

            elif "dirname" in children:
                with open(path.join(self.fullPath, children["dirname"] + ".dir.codegenpt"), 'w+') as file:
                    file.write('@include .codegenpt.json\n' + children["prompt"])
                    dir = CodeGenPTDirectory(self.fullPath + os.sep + children["dirname"])
                    dir.create(children)