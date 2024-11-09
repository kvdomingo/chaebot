from asyncpraw import Reddit

from autocomeback.config import settings


async def get_reddit_client():
    return Reddit(
        client_id=settings.REDDIT_CLIENT_ID,
        client_secret=settings.REDDIT_CLIENT_SECRET,
        user_agent=settings.REDDIT_API_USER_AGENT,
    )
