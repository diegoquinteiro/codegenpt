from codegenpt.codegenpt_file import CodeGenPTFile
from codegenpt.commands.commands import Commands
from codegenpt.llm.llm import askLLM

system_message = """\
You are a file generator that follows strict commands. 

If the input starts with @generate, I'll provide instructions for the creation of \
a single file and you will output only the raw file content, without any instructions or comments.

If the input starts with @command, you should learn the new command and respond with OK.

Example input:
@command
Respond with "Hello!"

Example output:
Hello!\

Example input:
@generate
- Path: project/src
- Name: main.py
- Extension: py
Write a hello world program.

Example output:
print('hello world')
"""

user_message_template = """\
@generate
- Path: {path}
- Name: {basename}
- Extension: {extension}
{prompt}\
"""

def generate_file(file: CodeGenPTFile):
    user_message = user_message_template.format(
        path=file.path,
        basename=file.basename,
        extension=file.extension,
        prompt=file.prompt
    )

    messages = [
        {
            "role": "system",
            "content": system_message,
        },
        {
            "role": "user",
            "content": user_message,
        }
    ]

    for command in file.commands:
        messages = Commands.run(command=command, instructions=file, messages=messages)

    response = askLLM(messages=messages)

    return response
    