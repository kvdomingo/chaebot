from pathlib import Path

from loguru import logger

from .utils import get_secret_string

BASE_DIR = Path(__file__).parent.parent

GCP_PROJECT = "my-projects-306716"


def make_dotenv():
    env = get_secret_string("KVISUALBOT")
    with open(BASE_DIR / ".env", "w+") as f:
        f.write(env)
    logger.info(".env ok")


if __name__ == "__main__":
    make_dotenv()
