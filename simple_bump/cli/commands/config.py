import click


@click.group()
def config():
    """Configuration commands."""
    pass


@config.command()
def init():
    """Initializes a new configuration."""
    click.echo("Configuration initialized.")


@config.command()
def check():
    """Checks the current configuration."""
    click.echo("Configuration checked.")
