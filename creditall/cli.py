import click
import json
import os
import yaml
import sys

from click_default_group import DefaultGroup
from creditall.generate import render_output
from prompt_toolkit import prompt


def read_rcdata(path=os.getcwd()):
    filename = os.path.join(path, '.all-contributorsrc')

    # Check whether the rc file already exists
    if not os.path.exists('.all-contributorsrc'):
        click.echo('Please run the "init" command before any other command')
        sys.exit(1)

    # Read the rcdata
    with open('.all-contributorsrc', 'r') as rcfile:
        return json.load(rcfile)


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

    # Locate the roles.yaml file on the file system and add it to the data
    path, _ = os.path.split(__file__)
    with open(os.path.join(path, "roles.yaml")) as rolesfiles:
        data["types"] = yaml.safe_load(rolesfiles)["roles"]

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
    # Read the current configuration file
    rcdata = read_rcdata()

    # Collect data about the new contributor
    data = {}
    data["name"] = prompt('What is the name of the contributor? ')
    contrib = prompt('What are the contribution types for this contributor? (comma separated list) ')
    data["contributions"] = [c.strip() for c in contrib.split(",")]

    # Add the new contributor data
    rcdata["contributors"].append(data)

    # Write out the new data
    with open('.all-contributorsrc', 'w') as rcfile:
        json.dump(rcdata, rcfile, indent=2)


@click.command()
@click.argument('path', type=click.Path(exists=True), default=os.getcwd())
def readme(path):
    rcdata = read_rcdata(path)

    # Iterate over the target files that have been specified in the configuration
    for target in rcdata.get("files", ["README.md"]):
        targetfilename = os.path.join(path, target)

        # Read the file header and footers:
        header = []
        footer = []
        with open(targetfilename, 'r') as targetfile:
            for line in targetfile:
                if line.startswith('<!-- ALL-CONTRIBUTORS-LIST:START'):
                    break
                header.append(line)

            for line in targetfile:
                if line.startswith('<!-- ALL-CONTRIBUTORS-LIST:END'):
                    break

            for line in targetfile:
                footer.append(line)

        # Rewrite the README file
        with open(targetfilename, 'w') as targetfile:
            for line in header:
                targetfile.write(line)

            targetfile.write('<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->\n')
            targetfile.write(render_output(os.path.join(path, '.all-contributorsrc'), "README.md", None))
            targetfile.write('<!-- ALL-CONTRIBUTORS-LIST:END -->\n')

            for line in footer:
                targetfile.write(line)


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


@click.command()
@click.argument('path', type=click.Path(exists=True), default=os.getcwd())
def csv(path):
    # Find the .all-contributorsrc file
    filename = os.path.join(path, '.all-contributorsrc')
    if not os.path.exists(filename):
        raise FileNotFoundError(f'No .all-contributorsrc file found at {filename}')

    # Define a name for the output - could be made configurable later
    outputfile = os.path.join(os.getcwd(), "contributors.csv")

    # Render the Jinja2 template with the given data
    render_output(
        filename,
        "contributors.csv",
        outputfile
    )


# Construct nested commands
@click.group(cls=DefaultGroup, default='readme', default_if_no_args=True)
def generate():
    pass


generate.add_command(readme)
generate.add_command(publication)
generate.add_command(csv)


@click.group()
def cli():
    pass


cli.add_command(init)
cli.add_command(generate)
cli.add_command(check)
cli.add_command(add)


if __name__ == '__main__':
    cli()
