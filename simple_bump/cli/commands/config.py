import click


# Defining a command group for config commands
@click.group()
def config():
    """Configuration commands."""
    pass


# Defining the init subcommand under config
@config.command()
def init():
    """Initializes a new configuration."""
    click.echo("Configuration initialized.")


# Defining the check subcommand under config
@config.command()
def check():
    """Checks the current configuration."""
    click.echo("Configuration checked.")
