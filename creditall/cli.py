import click
from click_default_group import DefaultGroup


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
    click.echo('Doing all-contributors "check"...')


@click.command()
def add():
    click.echo('Doing all-contributors "add"...')


@click.command()
def readme():
    click.echo('Generating the files that all-contributors would generate')


@click.command()
def publication():
    click.echo('Generating a snippet for a publication')


# Construct nested commands
generate.add_command(readme)
generate.add_command(publication)

cli.add_command(init)
cli.add_command(generate)
cli.add_command(check)
cli.add_command(add)


if __name__ == '__main__':
    cli()
