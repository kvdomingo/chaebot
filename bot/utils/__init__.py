from bot.utils.generate_embed import SeverityLevel, generate_embed
from bot.utils.generate_schedule_fields import generate_schedule_fields


def escape_quote(queries: list[str] | tuple[str]) -> list[str]:
    return [
        f"""{query.replace('"', "").replace("'", "").replace("’", "")}"""
        for query in queries
    ]


__all__ = [
    "escape_quote",
    "generate_embed",
    "generate_schedule_fields",
    "SeverityLevel",
]
