from typing import Union, List, Tuple, Dict


def escape_quote(queries: Union[List[str], Tuple[str]]) -> List[str]:
    return [f"""{query.replace('"', "").replace("'", "").replace("’", "")}""" for query in queries]


def query_string_from_dict(query_dict: Dict):
    return '&'.join([f'{k}={v}' for k, v in query_dict.items()])
