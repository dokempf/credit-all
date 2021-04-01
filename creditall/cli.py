import click
import json
import os
from click_default_group import DefaultGroup
from creditall.generate import render_output
from prompt_toolkit import prompt


@click.command()
def init():
    # Check whether the rc file already exists
    if os.path.exists('.all-contributorsrc'):
        click.echo('File .all-contributorsrc already exists - not initializing')
        return

    # Create the data structure that serializes into a simple rcfile
    data = {}

    # We can add many prompts here, but I would like to keep it
    # minimalistic for now
    data["projectName"] = prompt("What's the name of the repository? ")

    # TODO: Add the taxonomy!

    # Already add the contributors field - although empty
    data["contributors"] = []

    # Write the actual rc file
    with open('.all-contributorsrc', 'w') as rcfile:
        json.dump(data, rcfile, indent=2)


@click.command()
def check():
    click.echo('The "check" functionality of the all-contributors CLI is currently not available in creditall...')


@click.command()
def add():
    # Check whether the rc file already exists
    if not os.path.exists('.all-contributorsrc'):
        click.echo('Please run the "init" command before the add command')
        return

    # Collect data about the new contributor
    data = {}
    data["name"] = prompt('What is the name of the contributor? ')
    data["contributions"] = prompt('What are the contribution types for this contributor? (comma separated list)').split(",")

    # Update the data file
    with open('.all-contributorsrc', 'r') as rcfile:
        rcdata = json.load(rcfile)

    # Add the new contributor data
    rcdata["contributors"].append(data)

    # Write out the new data
    with open('.all-contributorsrc', 'w') as rcfile:
        json.dump(rcdata, rcfile, indent=2)


@click.command()
@click.argument('path', type=click.Path(exists=True), default=os.getcwd())
def readme(path):
    click.echo('This should generate the README bits, but does not yet')


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
@click.group(cls=DefaultGroup, default='readme', default_if_no_args=True)
def generate():
    pass


generate.add_command(readme)
generate.add_command(publication)



@click.group()
def cli():
    pass


cli.add_command(init)
cli.add_command(generate)
cli.add_command(check)
cli.add_command(add)


if __name__ == '__main__':
    cli()
