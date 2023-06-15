from codegenpt.codegenpt_directory import CodeGenPTDirectory
from codegenpt.codegenpt_file import CodeGenPTFile
from codegenpt.commands.commands import Commands
from codegenpt.llm.llm import askLLM

system_message = """\
You are a directory structure generator that follows strict commands. 

If the input starts with @command, you should learn the new command and respond with OK.

If the input starts with @generate, I'll provide instructions for the creation of \
a directory and you will output JSON listing the files and directories this directory should contain, \
without any instructions or comments. Write filenames relative to the directory you're describing, without path. \

Each file or directory in the list will have a name and a prompt that will be used to generate its content, \
and such prompt can use the following command:

@include <filepath> - Read the contents of the another file with the given relative <filepath> to be \
be added as context and referred in the prompt as @filepath. Use only to refer to files you've listed \
or present in the context.

You will list all files necessary, but you can include directory entries without children with a prompt for future generation.
Write detailed prompts for what's necessary for files.

The content of the JSON you'll respond will be automatically included in the context and can itself be referenced on prompts as @.codegenpt.json.

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
    "type": "directory",
    "dirname": "quiz",
    "prompt": "Create the root directory of a command line quiz game using click.",
    "chidren": [
        {
            "type": "file",
            "filename": "main.py",
            "prompt": "Create the main file for the game.",
        },
        {
            "type": "file",
            "filename": "pyproject.toml",
            "prompt": "Configure the project using click as a dependecy.",
        },
        {
            "type": "file",
            "filename": "README.md",
            "prompt": "Create a README.md file for the project.",
        },
        {
            "type": "file",
            "filename": "quiz.json",
            "prompt": "Create a JSON with 100 questions in the format: { "questions": [{ "question": ..., "answers": [...], "correct_answer_index": [...] }, ...] }",
        },
        {
            "type": "directory",
            "dirname": "tests",
            "prompt": "Create a tests directory with tests for all .py files within the folders from @.codegenpt.json.",      
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
    