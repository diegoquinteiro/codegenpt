import os
import click
from codegenpt.codegenpt_file import CodeGenPTFile

from codegenpt.filesystem.file_discovery import find_codegenpt_files
from codegenpt.generators.file_generator import generate_file


@click.command()
@click.option('--recursive', '-R', is_flag=True, default=False, help='Find .codegenpt files in directories recursevily.')
@click.argument('path', default='.', type=click.Path(exists=True))
def cli(recursive, path):
    codegenpt(recursive=recursive, path=path)

def codegenpt(recursive=True, path='.'):
    if os.path.isdir(path):
        click.echo(f"🔎 Searching files...")
        files = find_codegenpt_files(recursive=recursive, path=path)
    else:
        files = [CodeGenPTFile(path)]
    
    for file in files:
        with file as file:
            click.echo(f"⏳ Generating file: {click.format_filename(file.filename)}")
            file.write(generate_file(file))
            click.echo(f"🍺 File generated: {click.format_filename(file.filename)}")
    
    click.echo(f"🍻 Success")

if __name__ == '__main__':
    cli()