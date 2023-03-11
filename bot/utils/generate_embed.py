from enum import Enum

from discord import Color, Embed


class SeverityLevel(Enum):
    ERROR = Color.red()
    WARNING = Color.gold()
    INFO = Color.blurple()
    SUCCESS = Color.green()


def generate_embed(
    title: str,
    content: str | list[str],
    severity: SeverityLevel,
    fields: dict = None,
    footer: str = None,
) -> Embed:
    if isinstance(content, list):
        content = "\n".join(content)
    embed = Embed(title=title, description=content, color=severity.value)
    if fields is not None:
        for key, val in fields.items():
            embed.add_field(name=key, value=str(val), inline=False)
    if footer is not None:
        embed.set_footer(text=footer)
    return embed
