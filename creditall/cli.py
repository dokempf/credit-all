import click
import os
from click_default_group import DefaultGroup
from creditall.generate import render_output


@click.group()
def cli():
    pass


@click.command()
def init():
    click.echo('Inititalizing')


@click.group(cls=DefaultGroup, default='readme', default_if_no_args=True)
def generate():
    pass


@click.command()
def check():
    click.echo('The "check" functionality of all-contributors CLI is currently not available in creditall...')


@click.command()
def add():
    click.echo('Doing all-contributors "add"...')


@click.command()
@click.argument('path', type=click.Path(exists=True), default=os.getcwd())
def readme(path):
    click.echo('Generating the files that all-contributors would generate')


@click.command()
@click.argument('path', type=click.Path(exists=True), default=os.getcwd())
def publication(path):
    # Find the .all-contributorsrc file
    filename = os.path.join(path, '.all-contributorsrc')
    if not os.path.exists(filename):
        raise FileNotFoundError(f'No .all-contributorsrc file found at {filename}')

    # Define a name for the output - could be made configurable later
    outputfile = os.path.join(os.getcwd(), "publication.tex")

    # Render the Jinja2 template with the given data
    render_output(
        filename,
        "publication.tex",
        outputfile
    )


# Construct nested commands
generate.add_command(readme)
generate.add_command(publication)

cli.add_command(init)
cli.add_command(generate)
cli.add_command(check)
cli.add_command(add)


if __name__ == '__main__':
    cli()
