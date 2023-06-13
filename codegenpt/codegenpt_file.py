from os import path
import shlex

from codegenpt.commands.command import Command

class CodeGenPTFile:

    @property
    def filename(self):
        return '.'.join(self.__filename.split('.')[:-1])
    
    @property
    def extension(self):
        return self.filename.split('.')[-1]
    
    @property
    def prompt(self):
        with open(self.__filename, 'r') as file:
            prompt_lines = list(filter(lambda line: not line.startswith('@'), file.readlines()))
            # Filter first lines if they are empty or whitespace
            while prompt_lines[0].strip() == '':
                prompt_lines.pop(0)

        return ''.join(prompt_lines)

    @property
    def commands(self):
        with open(self.__filename, 'r') as file:
            commands = list(map(
                lambda line: Command(
                    name = line.strip().split(' ')[0].replace('@', ''),
                    arguments = shlex.split(line.strip())[1:]
                ),
                list(filter(lambda line: line.startswith('@'), file.readlines()))
            ))
        return commands
        
    @property
    def path(self):
        return self.filename.split('/')[:-1]
    
    @property
    def basename(self):
        return path.basename(self.filename)
        
    @property
    def context(self):
        return {
            'basename': self.basename,
            'extension': self.extension,
            'path': self.path,
        }

    def __init__(self, filename):
        self.__filename = filename

    def write(self, content):
        with open(self.filename, "w+") as file:
            file.write(content)