import click


@click.group()
def manage():
    pass


@click.command()
def dbupdate():
    from src import update_or_create
    update_or_create.main()


@click.command()
@click.option('--limit', default=10)
@click.option('--channel', default=726831180565184603)
def download(limit, channel):
    from src import download
    download.main(limit, channel)


@click.command()
@click.argument('message')
def makemigrations(message):
    from src import makemigrations
    makemigrations.main(message)


@click.command()
def migrate():
    from src import migrate
    migrate.main()


@click.command()
def restart():
    from src import restart
    restart.main()


@click.command()
def runbot():
    from src import bot
    bot.run()


@click.command()
def shell():
    import subprocess
    subprocess.run('ipython', shell=True)


manage.add_command(dbupdate)
manage.add_command(download)
manage.add_command(makemigrations)
manage.add_command(migrate)
manage.add_command(restart)
manage.add_command(runbot)
manage.add_command(shell)

if __name__ == '__main__':
    manage()
