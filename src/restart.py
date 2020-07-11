import os
import subprocess


def main():
    cmd = (
        f"""curl -n -X DELETE https://api.heroku.com/apps/kvisualbot/dynos/worker -H "Content-Type: application/json" -H "Accept: application/vnd.heroku+json; version=3" -H "Authorization: Bearer {os.environ['SCHEDULER_OAUTH']}" """
    )
    subprocess.run(cmd, shell=True)


if __name__ == '__main__':
    main()
