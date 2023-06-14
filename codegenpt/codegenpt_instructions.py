from abc import ABC, abstractmethod
from os import path
import shlex
from codegenpt.commands.command import Command

class CodeGenPTInstructions(ABC):
        
    @property
    def fullPath(self):
        return '.'.join(self.instructions_filename.split('.')[:-1])

    @property
    def prompt(self):
        with open(self.instructions_filename, 'r') as file:
            prompt_lines = list(filter(lambda line: not line.startswith('@'), file.readlines()))
            # Filter first lines if they are empty or whitespace
            while prompt_lines[0].strip() == '':
                prompt_lines.pop(0)

        return ''.join(prompt_lines)

    @property
    def commands(self):
        with open(self.instructions_filename, 'r') as file:
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
        return self.instructions_filename.split('/')[:-1]
        
    @property
    @abstractmethod
    def context(self):
        pass

    def __init__(self, filename):
        self.instructions_filename = filename