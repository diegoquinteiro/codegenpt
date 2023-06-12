from codegenpt.codegenpt_file import CodeGenPTFile
from codegenpt.llm.llm import askLLM

system_message = """\
You are a file generator. I'll provide instructions for the creation of a single file
on each message and you will output the file content, without explanations.
The instructions will be in the following format:

Example input:
- Path: project/srt
- Name: main.py
- Extension: py
Write a hello world program.

Example output:
print('hello world')
"""

user_message_template = """\
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

    response = askLLM([
        {
            "role": "system",
            "content": system_message,
        },
        {
            "role": "user",
            "content": user_message,
        }
    ])

    return response
    