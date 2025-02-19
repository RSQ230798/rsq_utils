import re
from typing import List 

def clean_path(path: str) -> str:
    """
    clean a path string by removing leading and trailing slashes and adding a trailing slash if the path does not have an extension.

    Example:
    >>> clean_path("/api/v1/")
    "api/v1/"
    >>> clean_path("/api/v1")
    "api/v1/"
    """
    if path.startswith("/"):
        path = path[1:]
    
    if not path.endswith("/"):
        if "." not in path:
            path += "/"

    if "." in path:
        if path.endswith("/"):
            path = path[:-1]

    return path


def find_template_params(template: str) -> List[str]:
    """
    Finds the parameters in a path template string.

    Example:
    >>> find_template_params("/api/{version}/{resource}")
    ["version", "resource"]
    """
    pattern = r'{([^}]*)}'
    matches = re.finditer(pattern, template)
    
    params: List[str] = [match.group(1) for match in matches]
    
    return params


