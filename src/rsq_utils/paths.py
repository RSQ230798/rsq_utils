import re
from typing import List 

def clean_path(path):
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
    
    params = [match.group(1) for match in matches]
    
    return params


