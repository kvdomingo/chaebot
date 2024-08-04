import re
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


def make_dotenvrc():
    with open(BASE_DIR / ".env") as f:
        env = f.readlines()
    for i, line in enumerate(env):
        if len(line) > 0 and not re.match(r"^\s+$", line):
            env[i] = f"export {line}"
    with open(BASE_DIR / ".envrc", "w+") as f:
        f.writelines(env)


if __name__ == "__main__":
    make_dotenvrc()
