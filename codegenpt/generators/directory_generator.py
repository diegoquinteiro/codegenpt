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

Each file or directory in the list will have a name and a prompt that will be used to generate its content. \

- Only text files are supported, you cannot create images or other binary files.
- Files will be small at 1000 words at maximum, so break them up in multiple files if necessary.
- You will list all files necessary, but you can include directory entries without children with a prompt for future generation.
- You will write detailed prompts for what's necessary for files. 
- You will list the dependencies for each file and directory, and they will be generated before the file or directory that depends on them.
    - The dependencies list should include the relative path to the file or directory.
    - If a file content is relevant to generate the content of another file, you should include it as a dependency.
        - For example, if you're generating a README.md file, you should include the main.py file as a dependency so the functionalities can be described.
        - For example, if you're generating a test_main.py file, you should include the main.py file as a dependency so the tests can be written.
        - For example, if you're generating a CSS file to style a html file, you should include the html file as a dependency so the CSS can be written. 
    - You will not create circular dependencies
    - You can reference dependencies in the prompt using @<dependency_path>, where <dependency_path> is the relative path to the dependency.

The content of the JSON you'll respond will be automatically included in the context and can itself be referenced on prompts as @.codegenpt.json.

Example input:
@command
Respond with "Hello!"

Example output:
Hello!\

Example input:
@generate
- Path: .
- Name: tic-tac-toe
Create a tic-tac-toe game using HTML, CSS and JavaScript.

Example output:
{
    "children": [
        {
            "filename": "index.html",
            "prompt": "Create the HTML structure for the game.",
            "type": "file"
        },
        {
            "filename": "style.css",
            "dependencies": [
                "index.html",
                "game.js"
            ],
            "prompt": "Create the CSS styles for the tic-tac-toe board and other game elements.",
            "type": "file"
        },
        {
            "filename": "game.js",
            "dependencies": [
                "index.html"
            ],
            "prompt": "Create the JS logic for the game. Include functions to check for win/loss, to switch turns and to draw the game board.",
            "type": "file"
        },
        {
            "dependencies": [
                "index.html",
                "game.js"
            ],
            "filename": "README.md",
            "prompt": "Write instructions for playing the game.",
            "type": "file"
        },
        {
            "children": [
                {
                    "filename": "test_game.js",
                    "dependencies": [
                        "../game.js"
                    ],
                    "prompt": "Create tests for the function in @../game.js.",
                    "type": "file"
                }
            ],
            "dirname": "tests",
            "prompt": "Create tests for the game logic.",
            "type": "directory"
        }
    ],
    "dirname": "tic-tac-toe",
    "prompt": "Create a tic-tac-toe game using HTML, JS and CSS.",
    "type": "directory"
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
    