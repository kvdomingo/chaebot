from .convenience import ping, purge
from .query import list_, query, spam
from .twitter import twitter

COMMANDS_TO_LOAD = [ping, purge, query, spam, list_, twitter]
