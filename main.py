import asyncio

import click


@click.group()
def manage():
    pass


@click.command()
@click.option("--limit", default=10)
def download(limit):
    from src import download

    download.main(limit)


@click.command()
def runbot():
    from bot import bot

    asyncio.run(bot.main())


manage.add_command(download)
manage.add_command(runbot)


if __name__ == "__main__":
    manage()
