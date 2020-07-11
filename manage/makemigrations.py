import subprocess
from dotenv import load_dotenv
load_dotenv()


def main(commit_message):
    if commit_message is not None and len(commit_message) > 0:
        subprocess.run(f""" alembic revision --autogenerate -m "{commit_message}" """, shell=True)
    else:
        subprocess.run("alembic revision --autogenerate", shell=True)


if __name__ == '__main__':
    main(commit_message)
