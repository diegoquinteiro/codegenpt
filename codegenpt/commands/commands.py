from codegenpt.codegenpt_instructions import CodeGenPTInstructions
from codegenpt.commands.include import include
from codegenpt.commands.command import Command


class Commands:
    commandRunners = {}

    def registerCommandRunner(name, commandRunner):
        Commands.commandRunners[name] = commandRunner

    def run(command: Command, instructions: CodeGenPTInstructions,  messages):
        if command.name in Commands.commandRunners:
            return Commands.commandRunners[command.name](command, instructions, messages)
        return messages
    

Commands.registerCommandRunner('include', include)