import click


@click.group()
def manage():
    pass

@click.command()
@click.argument('message')
def makemigrations(message):
    from manage import makemigrations
    makemigrations.main(message)

@click.command()
def migrate():
    from manage import migrate
    migrate.main()

@click.command()
def dbupdate():
    from src import update_or_create
    update_or_create.main()

@click.command()
def restart():
    from src import restart
    restart.main()

@click.command()
def runbot():
    from src import kbot

manage.add_command(makemigrations)
manage.add_command(migrate)
manage.add_command(dbupdate)
manage.add_command(restart)
manage.add_command(runbot)


if __name__ == '__main__':
    manage()
