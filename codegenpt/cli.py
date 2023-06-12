import click

from codegenpt.filesystem.file_discovery import find_codegenpt_files
from codegenpt.generators.file_generator import generate_file


@click.command()
@click.option('--recursive', default=True, help='Find .codegenpt files in directories recursevily.')
def cli(recursive):
    codegenpt(recursive=recursive)

def codegenpt(recursive=True):
    click.echo(f"🔎 Searching files...")
    files = find_codegenpt_files(recursive=recursive)
    
    for file in files:
        with file as file:
            click.echo(f"⏳ Generating file: {click.format_filename(file.filename)}")
            file.write(generate_file(file))
            click.echo(f"🍺 File generated: {click.format_filename(file.filename)}")
    
    click.echo(f"🍻 Success")

if __name__ == '__main__':
    cli()