import click

from bot import bot
from src import download


@click.group()
def manage():
    pass


@click.command()
@click.option("--limit", default=10)
def download(limit):
    download.main(limit)


@click.command()
def runbot():
    bot.main()


manage.add_command(download)
manage.add_command(runbot)


if __name__ == "__main__":
    manage()
