from os import makedirs
def refine_path(path: str) -> str:
    """Refines the path string."""
    if path == '' or path is None:
        return ''
    res = path.replace('\\','/')
    if res[-1] == '/':
        res = res[:-1]
    return res
