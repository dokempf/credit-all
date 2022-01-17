import click
import yaml

from creditall.generate import render_file
from creditall.paths import (
    find_rolefile,
    have_allcontributorsrc,
    read_allcontributorsrc,
    write_allcontributorsrc,
)
from prompt_toolkit import prompt


@click.command()
def add():
    # Read the current all-contributorsrc file
    data = read_allcontributorsrc()

    # Collect data about the new contributor
    contrib_data = {}
    contrib_data["name"] = prompt("What is the name of the contributor? ")
    contrib = prompt(
        "What are the contribution types for this contributor? (comma separated list) "
    )
    contrib_data["contributions"] = [c.strip() for c in contrib.split(",")]

    # Add the new contributor data
    data["contributors"].append(contrib_data)

    # Write out the new data
    write_allcontributorsrc(data)


@click.command()
def check():
    click.echo(
        'The "check" functionality of the all-contributors CLI is currently not available in creditall...'
    )


@click.command()
def generate():
    data = read_allcontributorsrc()

    # Iterate over the given renderable files and process them
    for target in data.get("files", ["README.md"]):
        render_file(target)


@click.command()
def init():
    # If this is already initialized, we do nothing
    if have_allcontributorsrc():
        click.echo("File .all-contributorsrc already exists - not initializing")
        return

    # Create the data structure that serializes into a simple rcfile
    data = {}

    # We can add many prompts here, but I would like to keep it
    # minimalistic for now
    data["projectName"] = prompt("What's the name of the repository? ")

    # Locate the roles.yaml file on the file system and add it to the data
    with open(find_rolefile(), "r") as rolesfiles:
        data["types"] = yaml.safe_load(rolesfiles)["roles"]

    # Already add the contributors field - although empty
    data["contributors"] = []

    # Write the actual rc file
    write_allcontributorsrc(data)


@click.group()
def cli():
    # This is the main entry point command. It only dispatches to subcommands
    pass


# Register all subcommands. These are outlined in the all-contributors specification.
cli.add_command(init)
cli.add_command(generate)
cli.add_command(check)
cli.add_command(add)


if __name__ == "__main__":
    cli()
