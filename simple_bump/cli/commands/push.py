import click

from simple_bump.core.main import Core


@click.command()
@click.option('--tags', is_flag=True, help='Push tags along with changes.')
def push(tags):
    """Pushes changes to the repository."""
    core = Core()
    core.go.push_changes()
    # if tags:
    #     click.echo("Changes and tags pushed.")
    # else:
    #     click.echo("Changes pushed.")
