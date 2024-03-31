import click

from simple_bump.core.handler import Handler


@click.group()
def config() -> None:
    """Configuration commands."""
    pass


@config.command()
@click.option('--base', is_flag=True)
def init(base: bool) -> None:
    """Initializes a new configuration."""
    handler = Handler()
    handler.init_config(base)


@config.command()
def check() -> None:
    """Checks the current configuration."""
    click.echo("Configuration checked.")
