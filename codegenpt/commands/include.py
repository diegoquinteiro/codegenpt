from codegenpt.codegenpt_instructions import CodeGenPTInstructions
from codegenpt.commands.command import Command

command_message = '''\
@command
If the message starts with @include, I'll send the content of files
that can be included in future instructions, and you should respond with OK.

In future messages I'll reference the files with the following syntax:
@filename

Example input:
@include
- File name: ../lorem.txt
Lorem ipsum dolor sit amet.

Example output:
OK\

Example input:
@generate
The first word of the file @lorem.txt

Example output:
Lorem\
'''

user_message = '''\
@include
- File name: {file_name}
{file_content}\
'''

assistant_message = '''\
OK\
'''


def include(command: Command, instructions: CodeGenPTInstructions, messages):
    command_messages = [
        {
            "role": "user",
            "content": command_message,
        },
        {
            "role": "assistant",
            "content": assistant_message
        }
    ]

    for filename in command.arguments:
        if filename.startswith('/'):
            path = filename[1:].split('/')
        else:
            path = instructions.path + filename.split('/')

        with open('/'.join(path), 'r') as file:
            file_content = file.read()
            command_messages.append({
                "role": "user",
                "content": user_message.format(
                    file_name = filename,
                    file_content = file_content
                ),
            })

        command_messages.append({
            "role": "assistant",
            "content": assistant_message
        })

    return [messages[0]] + command_messages + messages[1:]
