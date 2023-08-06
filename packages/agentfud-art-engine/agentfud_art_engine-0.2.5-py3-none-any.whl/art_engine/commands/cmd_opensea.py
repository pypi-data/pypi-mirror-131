import click
from art_engine.engine import ArtEngine
import art_engine.appconfig as config
from rich.console import Console
from rich.table import Table


@click.group()
def cli():
    """
    Handles OpenSea repetitive tasks
    """
    pass

@click.command()
def generate_config():
    """
    Generates price configuration for an OpenSea collection
    """
    pass


@click.command()
def set_prices():
    """
    Sets prices on OpenSea for a particular collection
    """
    pass


cli.add_command(set_prices)
cli.add_command(generate_config)
