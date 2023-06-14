import os
from threading import Thread
import click
from codegenpt.codegenpt_file import CodeGenPTFile

from codegenpt.filesystem.file_discovery import find_codegenpt_files
from codegenpt.generators.file_generator import generate_file


@click.command()
@click.option('--recursive', '-R', is_flag=True, default=False, help='Find .codegenpt files in directories recursevily.')
@click.option('--force', '-f', is_flag=True, default=False, help='Overwrite existing files with new ones.')
@click.argument('path', default='.', type=click.Path(exists=True))
def cli(recursive, force, path):
    codegenpt(recursive=recursive, force=force, path=path)

def codegenpt(recursive=True, force=True, path='.'):
    if os.path.isdir(path):
        click.echo(f"🔎 Searching files...")
        files = find_codegenpt_files(recursive=recursive, path=path)
    else:
        files = [CodeGenPTFile(path)]
    
    generation_threads = [Thread(target=generate, args=(file, force)) for file in files]
    
    for thread in generation_threads:
        thread.start()

    for thread in generation_threads:
        thread.join()

    click.echo(f"🍻 Success")

def generate(file: CodeGenPTFile, force=True):
    if os.path.exists(file.fullPath) and not force:
        click.echo(f"👍 File already exists: {click.format_filename(file.fullPath)}")
        return
    click.echo(f"⏳ Generating file: {click.format_filename(file.fullPath)}")
    file.write(generate_file(file))
    click.echo(f"🍺 File generated: {click.format_filename(file.fullPath)}")

if __name__ == '__main__':
    cli()