from bot.utils.generate_embed import SeverityLevel, generate_embed


def escape_quote(queries: list[str] | tuple[str]) -> list[str]:
    return [f"""{query.replace('"', "").replace("'", "").replace("’", "")}""" for query in queries]


__all__ = [
    "escape_quote",
    "generate_embed",
    "SeverityLevel",
]
