def escape_quote(queries: list[str] | tuple[str]) -> list[str]:
    return [f"""{query.replace('"', "").replace("'", "").replace("’", "")}""" for query in queries]
