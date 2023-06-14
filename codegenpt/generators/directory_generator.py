from codegenpt.codegenpt_directory import CodeGenPTDirectory
from codegenpt.codegenpt_file import CodeGenPTFile
from codegenpt.commands.commands import Commands
from codegenpt.llm.llm import askLLM

system_message = """\
You are a directory generator that follows strict commands. 

If the input starts with @command, you should learn the new command and respond with OK.

If the input starts with @generate, I'll provide instructions for the creation of \
a directory and you will output JSON listing the files and directories this directory should contain, \
without any instructions or comments.

Each file or directory in the list will have a name and a prompt that will be used to generate its content, \
and such prompt can use the following command:

@include <filename> - Read the contents of the file with the given filename to be \
be added as context and referred in the prompt as @filename.

The content of the provided JSON will be automatically included in the context and can be referenced as @.codegenpt.json.

Example input:
@command
Respond with "Hello!"

Example output:
Hello!\

Example input:
@generate
- Path: .
- Name: quiz
Create a command line quiz game using click.

Example output:
{
    "dirname": "quiz",
    "prompt": "Create the root directory of a command line quiz game using click.",
    "chidren": [
        {
            "filename": "main.py",
            "prompt": "Create the main file for the game.",
        },
        {
            "filename": "pyproject.toml",
            "prompt": "Configure the project using click.",
        },
        {
            "filename": "README.md",
            "prompt": "Create a README.md file for the project.",
        },
        {
            "filename": "quiz.json",
            "prompt": "Create a JSON with 100 questions in the format: { "questions": [{ "question": ..., "answers": [...], "correct_answer_index": [...] }, ...] }",
        },
        {
            "dirname": "tests",
            "prompt": "Create a tests directory within @.codegenpt.json.",        
        }
    ]
}\
"""

user_message_template = """\
@generate
- Path: {path}
- Name: {basename}
{prompt}\
"""

def generate_directory(dir: CodeGenPTDirectory):
    user_message = user_message_template.format(
        path=dir.path,
        basename=dir.basename,
        prompt=dir.prompt
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

    for command in dir.commands:
        messages = Commands.run(command=command, instructions=dir, messages=messages)

    response = askLLM(messages=messages, json=True)

    return response
    