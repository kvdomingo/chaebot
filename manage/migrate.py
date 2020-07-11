import subprocess


def main():
    subprocess.run("alembic upgrade head", shell=True)


if __name__ == '__main__':
    main()
