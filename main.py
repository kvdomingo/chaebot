import click


@click.group()
def manage():
    pass


@click.command()
def dbdump():
    from scripts import dump_to_json
    dump_to_json.main()


@click.command()
def dbimport():
    from scripts import import_json
    import_json.main()


@click.command()
def dbupdate():
    from src import update_or_create
    update_or_create.main()


@click.command()
@click.option('--limit', default=10)
def download(limit):
    from src import download
    download.main(limit)


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
    from bot import bot
    bot.main()


@click.command()
def shell():
    import subprocess
    subprocess.run('ipython', shell=True)


manage.add_command(dbdump)
manage.add_command(dbimport)
manage.add_command(dbupdate)
manage.add_command(download)
manage.add_command(makemigrations)
manage.add_command(migrate)
manage.add_command(restart)
manage.add_command(runbot)
manage.add_command(shell)

if __name__ == '__main__':
    manage()
