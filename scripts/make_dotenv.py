from pathlib import Path

from loguru import logger
from mako.template import Template

from .utils import get_secret_string

BASE_DIR = Path(__file__).parent.parent

GCP_PROJECT = "my-projects-306716"


def make_dotenv():
    template = Template(filename=str(BASE_DIR / "scripts" / "templates" / ".env.mako"))
    env = template.render(
        SECRET_KEY=get_secret_string("SECRET_KEY"),
        SENTRY_DSN=get_secret_string("SENTRY_DSN"),
        TWITTER_ACCESS_KEY=get_secret_string("TWITTER_ACCESS_KEY"),
        TWITTER_ACCESS_SECRET=get_secret_string("TWITTER_ACCESS_SECRET"),
        TWITTER_CONSUMER_KEY=get_secret_string("TWITTER_CONSUMER_KEY"),
        TWITTER_CONSUMER_SECRET=get_secret_string("TWITTER_CONSUMER_SECRET"),
        DISCORD_TOKEN=get_secret_string("DISCORD_TOKEN"),
        DISCORD_ADMIN_ID=get_secret_string("DISCORD_ADMIN_ID"),
        DISCORD_TEST_GUILD_ID=get_secret_string("DISCORD_TEST_GUILD_ID"),
    )
    with open(BASE_DIR / ".env", "w+") as f:
        f.write(env)

    logger.info(".env ok")


if __name__ == "__main__":
    make_dotenv()
