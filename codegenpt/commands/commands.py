from codegenpt.codegenpt_file import CodeGenPTFile
from codegenpt.commands.include import include
from codegenpt.commands.command import Command


class Commands:
    commandRunners = {}

    def registerCommandRunner(name, commandRunner):
        Commands.commandRunners[name] = commandRunner

    def run(command: Command, file: CodeGenPTFile,  messages):
        if command.name in Commands.commandRunners:
            return Commands.commandRunners[command.name](command, file, messages)
        return messages
    

Commands.registerCommandRunner('include', include)