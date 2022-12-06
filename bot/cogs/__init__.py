from .convenience import ping, purge
from .query import list_, query, spam
from .twitter import twitter
from .vlive import vlive

COMMANDS_TO_LOAD = [ping, purge, query, spam, list_, twitter, vlive]
