import os
import sys
import subprocess
from dotenv import load_dotenv


load_dotenv()

def main():
    cmd = (
    f"""curl -n -X DELETE https://api.heroku.com/apps/kvisualbot/dynos/worker -H "Content-Type: application/json" -H "Accept: application/vnd.heroku+json; version=3" -H "Authorization: Bearer {os.environ['SCHEDULER_OAUTH']}"
    """
    )
    subprocess.run(cmd, stdout=sys.stdout, stderr=sys.stderr, shell=True)


if __name__ == '__main__':
    main()
