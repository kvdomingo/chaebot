from .get_group_choices import get_group_choices


def escape_quote(queries: list[str] | tuple[str]) -> list[str]:
    return [f"""{query.replace('"', "").replace("'", "").replace("’", "")}""" for query in queries]


def query_string_from_dict(query_dict: dict):
    return "&".join([f"{k}={v}" for k, v in query_dict.items()])
