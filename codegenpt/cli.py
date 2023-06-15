import os
from threading import Thread
import click
from codegenpt.codegenpt_directory import CodeGenPTDirectory
from codegenpt.codegenpt_file import CodeGenPTFile

from codegenpt.filesystem.file_discovery import find_codegenpt_directories, find_codegenpt_files
from codegenpt.generators.directory_generator import generate_directory
from codegenpt.generators.file_generator import generate_file


@click.command()
@click.version_option()
@click.option('--recursive', '-R', is_flag=True, default=False, help='Find .codegenpt files in directories recursevily.')
@click.option('--iterations', '-i', default=3, help='Maximum iterations to run for generating files.')
@click.option('--force', '-f', is_flag=True, default=False, help='Overwrite existing files with new ones.')
@click.argument('path', default='.', type=click.Path(exists=True))
def cli(recursive=False, iterations=3, force=False, path='.'):
    codegenpt(recursive=recursive, iterations=iterations, force=force, path=path)


def codegenpt(recursive=True, iterations=1, force=True, path='.'):
    if os.path.isdir(path):
        click.echo(f"🔎 Searching files...")
        files = find_codegenpt_files(recursive=recursive, path=path)
        directories = find_codegenpt_directories(
            recursive=recursive, path=path)
    else:
        files = []
        directories = []
        if path.endswith('.dir.codegenpt'):
            directories = [CodeGenPTDirectory(path)]
        else:
            files = [CodeGenPTFile(path)]

    file_generation_threads = [Thread(target=generate_file_async, args=(file, force)) for file in files]
    directory_generation_threads = []
    recursion_threads = []
    thread_to_directory_mapping = {}
    for directory in directories:
        thread = Thread(target=generate_directory_async, args=(directory, force))
        directory_generation_threads.append(thread)
        thread_to_directory_mapping[thread.name] = directory

    for thread in file_generation_threads:
        thread.start()
    
    for thread in directory_generation_threads:
        thread.start()

    for thread in directory_generation_threads:
        thread.join()
        if iterations > 1:
            recursion_thread = Thread(target = codegenpt, kwargs={"recursive": True, "iterations": iterations -1, "force": force, "path": thread_to_directory_mapping[thread.name].fullPath})
            recursion_thread.start()
            recursion_threads.append(recursion_thread)

    for thread in file_generation_threads:
        thread.join()

    for thread in recursion_threads:
        thread.join()

    click.echo(f"🍻 Success")


def generate_file_async(file: CodeGenPTFile, force=True):
    if os.path.exists(file.fullPath) and not force:
        click.echo(
            f"👍 File already exists: {click.format_filename(file.fullPath)}")
        return
    click.echo(f"⏳ Generating file: {click.format_filename(file.fullPath)}")
    file.write(generate_file(file))
    click.echo(f"🍺 File generated: {click.format_filename(file.fullPath)}")


def generate_directory_async(directory: CodeGenPTDirectory, force=True):
    if os.path.exists(directory.fullPath) and not force:
        click.echo(
            f"👍 Directory already exists: {click.format_filename(directory.fullPath)}")
        return
    click.echo(
        f"⏳ Generating directory: {click.format_filename(directory.fullPath)}")
    directory.create(generate_directory(directory))
    click.echo(
        f"🍺 Directory generated: {click.format_filename(directory.fullPath)}")


if __name__ == '__main__':
    cli()
